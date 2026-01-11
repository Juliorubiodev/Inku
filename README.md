# 🏯 Inku - Plataforma de Lectura de Manga

**Inku** es una plataforma moderna y escalable para la lectura y gestión de mangas, construida con una arquitectura de microservicios y desplegada en la nube.

## 🌟 Características Principales

*   **Catálogo de Mangas**: Exploración fluida con búsqueda y filtrado.
*   **Lector PDF Integrado**: Visor optimizado para leer capítulos subidos en formato PDF.
*   **Gestión de Listas**: Crea listas personalizadas (públicas y privadas) para organizar tus lecturas.
*   **Autenticación Segura**: Sistema de login robusto integrado con Firebase Auth.
*   **Subida de Contenido**: Herramientas para que los administradores suban nuevos mangas y capítulos (con integración S3).

## 🛠️ Stack Tecnológico

### Frontend
- **React + Vite**: Rendimiento y experiencia de desarrollo moderna.
- **TypeScript**: Tipado estático para mayor robustez.
- **CSS Modules**: Estilos modulares y mantenibles.

### Backend (Microservicios)
- **Python + FastAPI**: Alto rendimiento y facilidad de desarrollo asíncrono.
- **Arquitectura**:
    - `manga-service`: Gestión de contenido (Mangas, Capítulos, Uploads).
    - `auth-service`: Gestión de usuarios y sesiones.
    - `list-service`: Listas de favoritos y colecciones de usuarios.
- **Firebase**: Autenticación y Base de Datos (Firestore).
- **AWS S3**: Almacenamiento escalable de archivos (PDFs, portadas).

### Infraestructura
- **Docker**: Contenerización de servicios.
- **Nginx**: API Gateway y Reverse Proxy (Entorno Local/VPS).
- **Render**: Plataforma de despliegue en la nube (Blueprints).

## 🚀 Despliegue

Consulta nuestros manuales detallados para poner en marcha el proyecto:

*   📄 **[Manual de Despliegue en Render (Producción)](docs/MANUAL_DESPLIEGUE_RENDER.md)**: Guía paso a paso para desplegar en la nube usando `render.yaml`.
*   💻 **[Manual de Despliegue Local](docs/MANUAL_DESPLIEGUE_LOCAL.md)**: Instrucciones para desarrollo local con Docker Compose.

## 📂 Estructura del Proyecto

```
Inku/
├── backend/            # Microservicios (FastAPI)
│   ├── manga-service/
│   ├── auth-service/
│   ├── list-service/
│   └── docker-compose.yml
├── frontend/           # Aplicación Web (React)
├── nginx/              # Configuración del Gateway
├── docs/               # Documentación y Manuales
├── render.yaml         # Blueprint para Render
└── README.md           # Este archivo
```

---
© 2026 Inku Project
