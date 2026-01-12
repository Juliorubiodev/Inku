class InkuUser(HttpUser):
    """Simula un usuario navegando por Inku."""
    
    wait_time = between(3, 6)
    
    @task(3)
    def get_mangas(self):
        """Obtener catálogo de mangas - alta frecuencia."""
        self.client.get("/api/mangas")
    
    @task(4)
    def get_health(self):
        """Health check - frecuencia media."""
        self.client.get("/api/health")
    
    @task(5)
    def get_manga_detail(self):
        """Obtener detalle de un manga específico."""
        # Intenta obtener el primer manga disponible
        self.client.get("/api/mangas/manga-1")


class ListServiceUser(HttpUser):
    """Simula un usuario interactuando con el servicio de listas."""
    
    wait_time = between(3, 7)
    host = "https://inku-list-service.onrender.com"
    
    @task(6)
    def get_public_lists(self):
        """Obtener listas públicas."""
        self.client.get("/api/lists/public")
    
    @task(7)
    def get_health(self):
        """Health check del list service."""
        self.client.get("/health")
