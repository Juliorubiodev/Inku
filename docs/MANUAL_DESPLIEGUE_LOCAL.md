# Manual de Despliegue Local (Desarrollo)

Este documento explica cómo desplegar la plataforma **Inku** en tu máquina local utilizando Docker Compose. También detalla el rol de Nginx en nuestra arquitectura.

## 📋 Prerrequisitos

1.  [Docker](https://www.docker.com/) y Docker Compose instalados.
2.  Credenciales de Firebase (`firebase-service-account.json`) ubicadas en la carpeta `backend/secrets/`.
3.  Archivos `.env` configurados en cada carpeta de servicio (`manga-service`, `auth-service`, `list-service`, `frontend`).

## 🏗️ Arquitectura Local con Nginx

En el entorno local, utilizamos una arquitectura con **API Gateway** implementada con Nginx.

### ¿Para qué usamos Nginx?
Nginx actúa como un proxy inverso (Reverse Proxy) que unifica todos nuestros microservicios bajo un solo puerto (el puerto 80 del contenedor, mapeado al puerto que desees, o manejado internamente).

**Funciones principales:**
1.  **Enrutamiento Unificado:**
    *   `/` -> Sirve el Frontend (Archivos estáticos React).
    *   `/api/mangas` -> Redirige al contenedor `manga-service:8000`.
    *   `/api/auth` -> Redirige al contenedor `auth-service:8000`.
    *   `/api/lists` -> Redirige al contenedor `list-service:8000`.
2.  **CORS Simplificado:** Al servir frontend y backend desde el mismo origen (mismo host/puerto visto desde el navegador), evitamos muchos problemas complejos de Cross-Origin Resource Sharing (CORS) durante el desarrollo.
3.  **Simulacro de Producción:** Nos acerca a una arquitectura real donde un balanceador de carga maneja las peticiones de entrada.

---

## 🚀 Pasos para el Despliegue

### 1. Configuración de Secretos
Asegúrate de que el archivo `backend/secrets/firebase-service-account.json` existe y es válido.

### 2. Construcción y Ejecución
Desde la carpeta `backend/` (donde está el `docker-compose.yml`), ejecuta:

```bash
docker-compose up --build
```

Esto levantará los siguientes contenedores:
- `manga-service` (Puerto 8001 -> 8000 interno)
- `auth-service` (Puerto 8003 -> 8000 interno)
- `list-service` (Puerto 8002 -> 8000 interno)
- *(Opcional)* Si tienes configurado un servicio `nginx` en compose, se levantará en el puerto 80.

*Nota: Actualmente el frontend se ejecuta normalmente con `npm run dev` en otro terminal para aprovechar el Hot Module Replacement (HMR) de Vite, comunicándose con los puertos expuestos de los microservicios (8001, 8002, 8003) definidos en tus variables de entorno locales.*

### 3. Ejecutar Frontend
En otro terminal, ve a la carpeta `frontend/`:

```bash
npm install
npm run dev
```

Accede a la aplicación en `http://localhost:5173`.

---

## 🧩 Estructura del Proyecto

- **backend/**: Contiene los microservicios Python/FastAPI.
    - `manga-service/`: Catálogo y Capítulos.
    - `auth-service/`: Autenticación e Integración Firebase.
    - `list-service/`: Gestión de Listas de Usuario.
    - `docker-compose.yml`: Orquestación de contenedores.
- **frontend/**: Aplicación React con Vite.
- **nginx/**: Configuración del Gateway (para producción simulada o despliegue en VPS).
