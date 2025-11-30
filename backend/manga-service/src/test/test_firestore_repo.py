import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# 1. Configuración del PATH para encontrar la carpeta 'inku_api'
# Asumiendo que ejecutas el test desde la raíz (donde están 'test' e 'inku_api' hermanas)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Importación del repositorio
try:
    # AQUI ESTA EL CAMBIO: inki -> inku
    # Asegúrate de que tu archivo en adapters se llame 'repo_firebase.py'
    from inku_api.adapters.repo_firebase import FirestoreMangaRepo
except ImportError as e:
    print(f"\n[ERROR] No se pudo importar 'inku_api'. Verifica que estás en la carpeta raíz.")
    print(f"Detalle del error: {e}\n")
    sys.exit(1)

class TestFirestoreMangaRepo(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.repo = FirestoreMangaRepo(self.mock_db)

    # -------------------------------------------------------------------------
    # TEST 1: Listar Mangas
    # Usamos @patch para evitar que Pydantic valide los datos falsos
    # IMPORTANTE: El string dentro de patch debe ser la ruta exacta donde SE USA la clase
    # -------------------------------------------------------------------------
    @patch('inku_api.adapters.repo_firebase.Manga') 
    def test_list_mangas(self, MockMangaClass):
        # 1. Mock de datos de Firestore
        mock_doc = MagicMock()
        mock_doc.id = "manga_1"
        mock_doc.to_dict.return_value = {
            "title": "Berserk",
            "description": "Dark Fantasy",
            "cover_path": "img.jpg",
            "recommended": "True", # Pydantic fallaría aquí, pero el Mock lo acepta
            "tags": ["seinen"]
        }
        
        self.mock_db.collection.return_value.stream.return_value = [mock_doc]

        # 2. Ejecutar
        results = list(self.repo.list_mangas())

        # 3. Verificar
        self.assertEqual(len(results), 1)
        
        # Verificamos que el repo llamó a la clase Manga con los datos correctos
        MockMangaClass.assert_called_once()
        kwargs = MockMangaClass.call_args[1]
        self.assertEqual(kwargs['title'], "Berserk")
        self.assertEqual(kwargs['id'], "manga_1")

    # -------------------------------------------------------------------------
    # TEST 2: Manga Existe
    # -------------------------------------------------------------------------
    def test_manga_exists(self):
        (self.mock_db.collection.return_value
         .document.return_value
         .get.return_value
         .exists) = True

        self.assertTrue(self.repo.manga_exists("manga_1"))

    # -------------------------------------------------------------------------
    # TEST 3: Listar Capítulos (Éxito)
    # -------------------------------------------------------------------------
    @patch('inku_api.adapters.repo_firebase.Chapter')
    def test_list_chapters_success(self, MockChapterClass):
        mock_doc = MagicMock()
        mock_doc.id = "ch_1"
        mock_doc.to_dict.return_value = {"number": 1, "title": "Intro", "manga_id": "m1"}

        col = (self.mock_db.collection.return_value
               .document.return_value
               .collection.return_value)
        
        # Simulamos éxito al ordenar
        col.order_by.return_value.stream.return_value = [mock_doc]

        results = list(self.repo.list_chapters("m1"))

        self.assertEqual(len(results), 1)
        MockChapterClass.assert_called() # Se instanció un capitulo

    # -------------------------------------------------------------------------
    # TEST 4: Fallback (Error en order_by)
    # -------------------------------------------------------------------------
    @patch('inku_api.adapters.repo_firebase.Chapter')
    def test_list_chapters_fallback_exception(self, MockChapterClass):
        col = (self.mock_db.collection.return_value
               .document.return_value
               .collection.return_value)

        # Simulamos que Firestore falla al ordenar (falta índice)
        col.order_by.side_effect = Exception("Falta índice compuesto")
        
        # Simulamos respuesta en el fallback (stream directo)
        mock_doc = MagicMock()
        mock_doc.id = "ch_1"
        mock_doc.to_dict.return_value = {"number": 1, "manga_id": "m1"}
        col.stream.return_value = [mock_doc]

        results = list(self.repo.list_chapters("m1"))

        self.assertEqual(len(results), 1)
        col.stream.assert_called() # Verifica que usó el plan B (sin ordenar)

    # -------------------------------------------------------------------------
    # TEST 5: Obtener Capítulo por ID
    # -------------------------------------------------------------------------
    @patch('inku_api.adapters.repo_firebase.Chapter')
    def test_get_chapter_by_id_found(self, MockChapterClass):
        mock_snap = MagicMock()
        mock_snap.exists = True
        mock_snap.id = "ch_1"
        mock_snap.to_dict.return_value = {"number": 10, "manga_id": "m1"}

        (self.mock_db.collection.return_value
         .document.return_value
         .collection.return_value
         .document.return_value
         .get.return_value) = mock_snap

        # Configuramos el objeto mock que devuelve la clase Chapter
        mock_instance = MagicMock()
        mock_instance.number = 10
        MockChapterClass.return_value = mock_instance

        chapter = self.repo.get_chapter_by_id("m1", "ch_1")
        
        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.number, 10)

if __name__ == '__main__':
    unittest.main()