# Manual de Despliegue en Render (Producción)

Este documento detalla los pasos para desplegar la plataforma **Inku** en Render.com utilizando la configuración de Blueprint (`render.yaml`).

## 📋 Prerrequisitos

1.  Una cuenta en [Render.com](https://render.com/).
2.  El código fuente subido a un repositorio de GitHub/GitLab conectado a tu cuenta de Render.
3.  El archivo `firebase-service-account.json` (credenciales de Firebase Admin SDK).

## 🚀 Arquitectura en Render

Para el despliegue en Render, utilizamos una arquitectura de **Microservicios Directos**. A diferencia del entorno local, en Render no utilizamos Nginx como gateway, sino que cada servicio se expone directamente a través de HTTPS y el Frontend se comunica con ellos.

*   **Frontend**: Static Site (React/Vite)
*   **Manga Service**: Web Service (Docker)
*   **Auth Service**: Web Service (Docker)
*   **List Service**: Web Service (Docker)

---

## 🛠️ Pasos para el Despliegue

### 1. Preparar Secretos
Asegúrate de tener a mano el contenido de tu archivo de credenciales de Firebase y las claves de AWS S3 (si usas almacenamiento S3).

### 2. Crear Blueprint en Render
1.  En el Dashboard de Render, haz clic en **New +** y selecciona **Blueprint**.
2.  Conecta tu repositorio de GitHub.
3.  Render detectará automáticamente el archivo `render.yaml` en la raíz del proyecto.

### 3. Configurar Variables de Entorno (Secrets)
Render te pedirá que ingreses los valores para las variables marcadas como `sync: false` en el `render.yaml`. Debes rellenar:

| Variable | Descripción |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | Tu Key ID de AWS (para subida de mangas). |
| `AWS_SECRET_ACCESS_KEY` | Tu Secret Key de AWS. |
| `AWS_S3_BUCKET` | El nombre de tu bucket S3. |
| `VITE_FIREBASE_API_KEY` | API Key pública de Firebase (Frontend). |
| `VITE_FIREBASE_AUTH_DOMAIN` | Auth Domain de Firebase. |
| `VITE_FIREBASE_PROJECT_ID` | Project ID de Firebase. |
| `VITE_FIREBASE_APP_ID` | App ID de Firebase. |

### 4. Configurar el Archivo de Servicio de Firebase
El `render.yaml` espera que el archivo de credenciales de Firebase esté en `/secrets/firebase-service-account.json` para todos los servicios backend.

1.  En la configuración del Blueprint (o editando cada servicio individual después de la creación inicial si el Blueprint falla):
2.  Ve a la sección **Environment** -> **Secret Files**.
3.  Añade un archivo llamado `firebase-service-account.json`.
4.  Pega el contenido completo de tu JSON de credenciales.
5.  Asegúrate de que la ruta de montaje sea `/secrets/firebase-service-account.json`.

*(Nota: En la primera ejecución del Blueprint, Render puede fallar si no encuentra este archivo. Es recomendable crear primero un "Environment Group" en Render con este archivo secreto y vincularlo en el `render.yaml` o configurarlo manualmente tras el primer intento).*

### 5. Despliegue
Haz clic en **Apply**. Render comenzará a construir y desplegar:
- `inku-manga-service`
- `inku-auth-service`
- `inku-list-service`
- `inku-frontend`

### 6. Verificación de URLs
Una vez desplegado:
1.  Verifica las URLs asignadas a cada servicio (ej: `https://inku-manga-service-xyz.onrender.com`).
2.  Asegúrate de que las variables de entorno del Frontend (`VITE_API_BASE_URL`, etc.) coincidan con estas URLs. Si Render asignó nombres diferentes, deberás actualizar las variables de entorno del servicio `inku-frontend` y redeployar.

---

## ⚠️ Notas Importantes
- **CORS**: El backend está configurado para aceptar peticiones desde `https://inku-frontend.onrender.com`. Si tu frontend tiene otra URL, actualiza la variable `CORS_ORIGINS` en los servicios backend.
- **Base de Datos**: Este proyecto usa Firebase Firestore (NoSQL), por lo que no necesitas desplegar una base de datos SQL adicional.
