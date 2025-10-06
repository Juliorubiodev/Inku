# 🖋️ Inku — Lector y plataforma colaborativa de manga

## 📌 Descripción general del proyecto

**Inku** es una aplicación móvil desarrollada en **Kotlin** con **Jetpack Compose** cuyo objetivo principal es ofrecer una plataforma gratuita, fluida y colaborativa para la **lectura y distribución de mangas**.

El proyecto busca resolver la **falta de herramientas oficiales o gratuitas con catálogos amplios** de manga digital. Actualmente, las pocas opciones existentes son:
- Aplicaciones de pago que limitan el acceso al contenido.  
- Plataformas oficiales con catálogos reducidos (por ejemplo, *MANGA Plus by Shueisha*, que solo publica obras de su editorial).  
- Herramientas no oficiales o desactualizadas que ya no funcionan correctamente.  

No existe un **referente actual** que permita acceder libremente a obras diversas y, al mismo tiempo, crear un espacio seguro para autores y lectores.  
Por ello, **Inku** representa una **oportunidad de mercado real**, al posicionarse como una **librería compartida** en la que, **bajo supervisión y revisión de un administrador**, los usuarios pueden subir sus series o libros favoritos, garantizando el cumplimiento de normas y evitando contenido indebido.

---

## 🎯 Problema que resuelve

El ecosistema actual de lectura de manga digital presenta varias limitaciones:

- 🔒 **Acceso restringido o pago obligatorio** para la mayoría de catálogos.  
- 🚫 **Ausencia de herramientas que permitan subir y compartir obras propias.**  
- ⚠️ **Publicidad excesiva o mal rendimiento** en las apps disponibles.  
- ❌ **Carencia de proyectos activos o mantenidos en el tiempo.**

**Inku** propone una alternativa **gratuita, moderna y colaborativa**, centrada en la comunidad y en la experiencia del lector.  
Los usuarios podrán:

1. 📖 **Leer mangas y libros** almacenados en la nube (formato PDF o imágenes).  
2. ☁️ **Subir sus propias creaciones** o compartir obras libres, bajo revisión de un administrador.  
3. 🚀 **Disfrutar de una lectura fluida, sin publicidad** y con soporte para favoritos, progreso y temas visuales.

---

## ⚙️ En qué se basa el proyecto

El desarrollo se apoya en las tecnologías y prácticas más recientes del ecosistema Android:

- **Jetpack Compose** para interfaces declarativas, reactivas y adaptativas.  
- **Kotlin** como lenguaje principal, por su robustez y soporte multiplataforma.  
- **AWS S3** como servicio de almacenamiento en la nube, para alojar los mangas de forma segura y escalable.  
- **Firebase / Ktor (Kotlin)** como backend planificado para manejar usuarios, metadatos y control de contenido.  
- **Arquitectura limpia (Clean Architecture)** y **patrón MVVM**, garantizando mantenibilidad y separación de responsabilidades.

---

## 📚 Referencias y antecedentes

El proyecto es de carácter **personal**, aunque nace de una observación técnica y de mercado.  
Se inspira en experiencias previas en desarrollo Android y en plataformas del sector como:

- [MangaDex](https://mangadex.org) — comunidad internacional de manga open source.  
- [MANGA Plus by Shueisha](https://mangaplus.shueisha.co.jp/updates) — aplicación oficial con obras limitadas a una sola editorial.  
- *AniMotion* — aplicación previa creada junto con un compañero para streaming de anime, que sirvió de referencia conceptual.  

Estas herramientas muestran enfoques distintos, pero ninguna aborda completamente la lectura colaborativa de mangas independientes en un entorno controlado.

---

## 🧠 Objetivos principales

- 🧩 Diseñar una **aplicación Android moderna, funcional y escalable**.  
- 📚 Implementar un **lector de PDF interno optimizado para manga**.  
- ☁️ Permitir la **subida de obras por parte de usuarios autenticados**, bajo supervisión.  
- 🔐 Integrar servicios cloud (AWS) y almacenamiento seguro.  
- 🧱 Mantener una **arquitectura modular, limpia y mantenible**.  
- 🌍 Crear una **comunidad global de lectores y autores** en torno al manga digital libre.

---

## 📱 Características principales

- 📚 **Lector de PDF integrado** para lectura fluida.  
- ☁️ **Sincronización con AWS S3**.  
- 🔍 **Explorador de mangas** con filtros y categorías.  
- ❤️ **Favoritos y progreso de lectura** guardados localmente.  
- ✍️ **Subida y gestión de obras propias.**  
- 🌙 **Modo oscuro** para lectura nocturna.  
- 🛡️ **Moderación de contenido** para mantener un entorno seguro.

---

## 🪣 Tecnologías principales

| Módulo | Tecnología / Herramienta |
|:--------|:--------------------------|
| Aplicación móvil | Kotlin + Jetpack Compose |
| API REST (backend) | Firebase + Kotlin Ktor | 
| Almacenamiento | AWS S3 |
| Base de datos | PostgreSQL / Supabase |
| Autenticación | JWT / Firebase Auth |
| Control de versiones | Git + GitHub |
| IDE | Android Studio |

---

## 🎨 Identidad visual

- **Color principal:** `#E63946` (rojo tinta japonesa)  
- **Fondo:** `#0E0E10` (oscuro, lectura inmersiva)  
- **Tipografía:** Poppins / Noto Sans JP  
- **Estilo:** minimalista, moderno, de inspiración japonesa

> “Inku” viene de *ink* (tinta) + pronunciación japonesa.  
> Representa la unión entre **tradición (manga clásico)** y **tecnología moderna**.