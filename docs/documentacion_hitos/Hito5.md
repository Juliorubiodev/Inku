# Hito 5: Despliegue de la Aplicación en un PaaS

En este hito se ha realizado el despliegue completo de la plataforma **Inku** en la nube utilizando **Render** como Platform as a Service (PaaS). Además, se han implementado herramientas de observabilidad y se han realizado pruebas de prestaciones.

---

## 📋 Índice

1. [Criterios de Selección del PaaS](#1-criterios-de-selección-del-paas)
2. [Herramientas de Despliegue](#2-herramientas-de-despliegue)
3. [Configuración del Despliegue Automático](#3-configuración-del-despliegue-automático)
4. [Herramientas de Observabilidad](#4-herramientas-de-observabilidad)
5. [Funcionamiento del Despliegue](#5-funcionamiento-del-despliegue)
6. [Pruebas de Prestaciones](#6-pruebas-de-prestaciones)

---

## 1. Criterios de Selección del PaaS

### 1.1 Opciones Evaluadas

Se evaluaron las siguientes plataformas para el despliegue:

| Plataforma | Pros | Contras | Decisión |
|------------|------|---------|----------|
| **Render** | Blueprint IaC, Free tier, Deploy desde GitHub, Región EU | Cold starts en free tier | ✅ **Seleccionado** |
| **Railway** | UI moderna, buena DX | Límites de uso más restrictivos | ❌ |
| **Fly.io** | Edge computing, baja latencia | Configuración más compleja | ❌ |
| **Heroku** | Madurez, documentación | Sin tier gratuito | ❌ |
| **Google Cloud Run** | Escalado automático | Complejidad de configuración inicial | ❌ |
| **AWS ECS/Fargate** | Flexibilidad total | Curva de aprendizaje alta, costos | ❌ |

### 1.2 Justificación de la Elección: Render

Se seleccionó **Render** por cumplir los tres requisitos obligatorios:

#### ✅ Requisito 1: Configuración como Código (IaC)

Render soporta **Blueprints** mediante el archivo `render.yaml`, que permite definir toda la infraestructura de forma declarativa:

```yaml
# render.yaml - Extracto
services:
  - type: web
    name: inku-manga-service
    runtime: docker
    dockerfilePath: ./backend/manga-service/Dockerfile.render
    dockerContext: ./backend
    region: frankfurt
    plan: free
    healthCheckPath: /api/health
    envVars:
      - key: CORS_ORIGINS
        value: https://inku-frontend.onrender.com
```

> **Reproducibilidad**: Cualquier persona con acceso al repositorio puede desplegar la misma infraestructura ejecutando el Blueprint.

#### ✅ Requisito 2: Despliegue Automático desde GitHub

Render se integra nativamente con GitHub:
- **Conexión directa**: El repositorio está vinculado a Render
- **Auto-deploy**: Cada push a `main` dispara un nuevo despliegue
- **Preview environments**: Los PRs pueden generar entornos de prueba

#### ✅ Requisito 3: Despliegue en Europa

Todos los servicios están desplegados en la región **Frankfurt (EU)**:

```yaml
region: frankfurt  # Cumple con GDPR y requisitos legales de la UE
```

### 1.3 Ventajas Adicionales de Render

| Característica | Beneficio |
|----------------|-----------|
| **Health Checks** | Monitorización automática de endpoints |
| **Zero-downtime deploys** | Despliegues sin interrupción del servicio |
| **Logs centralizados** | Visualización en tiempo real |
| **Métricas integradas** | CPU, memoria, latencia |
| **SSL automático** | Certificados Let's Encrypt incluidos |
| **Custom domains** | Soporte para dominios personalizados |

---

## 2. Herramientas de Despliegue

### 2.1 Stack de Despliegue

![Stack de Despliegue](docs/captures/SSH5/2.png)

### 2.2 Herramientas Utilizadas

| Herramienta | Función | Justificación |
|-------------|---------|---------------|
| **Docker** | Contenedorización | Reproducibilidad entre entornos |
| **GitHub Actions** | CI/CD Pipeline | Integración nativa con GitHub |
| **GitHub Packages** | Container Registry | Almacenamiento de imágenes Docker |
| **Render Blueprints** | Infrastructure as Code | Despliegue declarativo |
| **Render CLI** | Gestión desde terminal | Automatización avanzada |

### 2.3 Dockerfiles para Producción

Cada servicio tiene un `Dockerfile.render` optimizado para producción:

#### Manga Service Dockerfile
```dockerfile
# backend/manga-service/Dockerfile.render
FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/manga-service/src:/app/shared

WORKDIR /app

COPY manga-service/requirements.txt ./manga-service/
RUN pip install --upgrade pip && pip install -r manga-service/requirements.txt

COPY shared/ ./shared/
COPY manga-service/ ./manga-service/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "inku_api.main:app", \
     "--app-dir", "/app/manga-service/src", \
     "--host", "0.0.0.0", "--port", "8000"]
```

**Optimizaciones aplicadas:**
- `PYTHONDONTWRITEBYTECODE=1`: Evita archivos `.pyc`
- `PYTHONUNBUFFERED=1`: Logs en tiempo real
- Copia de dependencias antes del código (cache de layers)
- Módulo `shared` incluido en el contexto de build

---

## 3. Configuración del Despliegue Automático

### 3.1 render.yaml Completo

El archivo `render.yaml` define **toda** la infraestructura:

```yaml
# Render Blueprint Configuration
services:
  # =========================================================================
  # Manga Service API
  # =========================================================================
  - type: web
    name: inku-manga-service
    runtime: docker
    dockerfilePath: ./backend/manga-service/Dockerfile.render
    dockerContext: ./backend
    region: frankfurt
    plan: free
    healthCheckPath: /api/health
    envVars:
      - key: PYTHONPATH
        value: /app/manga-service/src:/app/shared
      - key: CORS_ORIGINS
        value: https://inku-frontend.onrender.com
      - key: FIREBASE_SERVICE_ACCOUNT_FILE
        sync: false  # Secret - se configura manualmente
      - key: AWS_ACCESS_KEY_ID
        sync: false
      - key: AWS_SECRET_ACCESS_KEY
        sync: false
      - key: S3_BUCKET
        sync: false
      - key: AWS_REGION
        value: eu-north-1

  # =========================================================================
  # Auth Service API
  # =========================================================================
  - type: web
    name: inku-auth-service
    runtime: docker
    dockerfilePath: ./backend/auth-service/Dockerfile.render
    dockerContext: ./backend
    region: frankfurt
    plan: free
    healthCheckPath: /health
    envVars:
      - key: PYTHONPATH
        value: /app/auth-service:/app/shared
      - key: CORS_ORIGINS
        value: https://inku-frontend.onrender.com
      - key: FIREBASE_SERVICE_ACCOUNT_PATH
        sync: false
      - key: FIREBASE_WEB_API_KEY
        sync: false

  # =========================================================================
  # List Service API
  # =========================================================================
  - type: web
    name: inku-list-service
    runtime: docker
    dockerfilePath: ./backend/list-service/Dockerfile.render
    dockerContext: ./backend
    region: frankfurt
    plan: free
    healthCheckPath: /health
    envVars:
      - key: PYTHONPATH
        value: /app/list-service/src:/app/shared
      - key: CORS_ORIGINS
        value: https://inku-frontend.onrender.com
      - key: FIREBASE_SERVICE_ACCOUNT_PATH
        sync: false

  # =========================================================================
  # Frontend (Static Site)
  # =========================================================================
  - type: web
    name: inku-frontend
    runtime: static
    buildCommand: cd frontend && npm ci && npm run build
    staticPublishPath: ./frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    headers:
      - path: /*
        name: Cache-Control
        value: public, max-age=31536000, immutable
    envVars:
      - key: VITE_API_BASE_URL
        value: https://inku-manga-service.onrender.com
      - key: VITE_AUTH_API_URL
        value: https://inku-auth-service.onrender.com
      - key: VITE_LIST_API_URL
        value: https://inku-list-service.onrender.com
      - key: VITE_FIREBASE_API_KEY
        sync: false
      - key: VITE_FIREBASE_AUTH_DOMAIN
        sync: false
      - key: VITE_FIREBASE_PROJECT_ID
        sync: false
      - key: VITE_FIREBASE_APP_ID
        sync: false
```

### 3.2 GitHub Actions Workflows

#### Workflow de Tests (`run_test.yml`)

```yaml
name: Project Tests

on:
  push:
    branches: ["main", "master"]
  pull_request:
    branches: ["main", "master"]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        service: [manga-service, auth-service, list-service]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          
      - name: Install Dependencies
        working-directory: ./backend/${{ matrix.service }}
        run: |
          pip install -r requirements.txt
          pip install pytest httpx pytest-mock

      - name: Run Tests
        env:
          FIREBASE_SERVICE_ACCOUNT_PATH: /fake/path.json
        run: |
          export PYTHONPATH="${GITHUB_WORKSPACE}/backend/${{ matrix.service }}/src:${GITHUB_WORKSPACE}/backend/shared"
          python -m pytest tests/ -v --tb=short

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          
      - name: Install & Test
        working-directory: ./frontend
        run: |
          npm install
          npm test -- --reporter=verbose
```

#### Workflow de Deploy (`deploy.yml`)

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### 3.3 Flujo de Despliegue

![Flujo de Despliegue](docs/captures/SSH5/3.png)

---

## 4. Herramientas de Observabilidad

### 4.1 Monitorización Implementada

| Herramienta | Tipo | Función |
|-------------|------|---------|
| **Render Metrics** | Métricas | CPU, memoria, latencia |
| **Render Logs** | Logs | Logs en tiempo real |
| **Health Checks** | Disponibilidad | Verificación de endpoints |
| **GitHub Actions** | CI/CD | Estado de builds y deploys |

### 4.2 Health Checks

Cada servicio expone un endpoint de health check:

```python
# Manga Service - /api/health
@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok", "service": "manga-service"}

# Auth Service - /health
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "auth-service"}

# List Service - /health
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "list-service"}
```

Render verifica estos endpoints cada **30 segundos** y reinicia el servicio si falla.

### 4.3 Logs Centralizados

Render proporciona visualización de logs en tiempo real:

![Logs](docs/captures/SSH5/4.png)
![Logs](docs/captures/SSH5/5.png)
![Logs](docs/captures/SSH5/6.png)

### 4.4 Métricas de Rendimiento

Las métricas disponibles en Render incluyen:

| Métrica | Descripción | Umbral Alerta |
|---------|-------------|---------------|
| **CPU Usage** | Uso de CPU | > 80% |
| **Memory Usage** | Uso de RAM | > 90% |
| **Response Time** | Latencia p95 | > 2000ms |
| **Request Rate** | Requests/min | Variable |
| **Error Rate** | % de errores | > 5% |

![Métricas](docs/captures/SSH5/metrics.png)
![Métricas](docs/captures/SSH5/metrics2.png)

---

## 5. Funcionamiento del Despliegue

### 5.1 URLs de los Servicios Desplegados

**Se debe tener en cuenta que al ser un servicio gratuito los servicios se desactivan despues de cierto tiempo de inactividad. Para activarlos se debe hacer acceder a cada url del servicio y dar click en iniciar, usualmente demora menos de 2 minutos o menos.**

| Servicio | URL | Estado |
|----------|-----|--------|
| 🌐 **Frontend** | https://inku-frontend.onrender.com | ✅ Activo |
| 📚 **Manga API** | https://inku-manga-service.onrender.com | ✅ Activo |
| 🔐 **Auth API** | https://inku-auth-service.onrender.com | ✅ Activo |
| 📝 **List API** | https://inku-list-service.onrender.com | ✅ Activo |

### 5.2 Verificación de Endpoints

#### Health Checks

```bash
# Manga Service
curl https://inku-manga-service.onrender.com/api/health
# Response: {"status":"ok","service":"manga-service"}

# Auth Service
curl https://inku-auth-service.onrender.com/health
# Response: {"status":"ok","service":"auth-service"}

# List Service
curl https://inku-list-service.onrender.com/health
# Response: {"status":"ok","service":"list-service"}
```

#### API Endpoints

```bash
# Obtener catálogo de mangas
curl https://inku-manga-service.onrender.com/api/mangas

# Obtener listas públicas
curl https://inku-list-service.onrender.com/api/lists/public
```

### 5.3 Capturas del Funcionamiento

![Frontend](docs/captures/SSH5/home.png)

![Lector](docs/captures/SSH5/lector.png)

![Listas](docs/captures/SSH5/listaspublicas.png)

![Listas](docs/captures/SSH5/mislistas.png)

![Subida](docs/captures/SSH5/subida.png)

![Deploy](docs/captures/SSH5/render.png)

---

## 6. Pruebas de Prestaciones

### 6.1 Herramientas de Testing

| Herramienta | Uso |
|-------------|-----|
| **Python Script** | Medición de latencia con `urllib` (`tests/load/latency_test.py`) |
| **Locust** | Pruebas de estrés distribuidas (`tests/load/locustfile.py`) |

### 6.2 Prueba de Latencia con Python

Se desarrolló un script Python personalizado para medir la latencia de todos los endpoints. El script realiza 5 requests a cada servicio y calcula estadísticas de latencia (mínima, promedio, máxima).

```bash
# Ejecutar prueba de latencia
python tests/load/latency_test.py
```

#### Resultados Obtenidos

| Endpoint | Min | Avg | Max | Success |
|----------|-----|-----|-----|---------|
| **Manga Health** | 166ms | 210ms | 294ms | 100% |
| **Auth Health** | 176ms | 4,646ms | 22,439ms | 100% |
| **List Health** | 182ms | 4,651ms | 22,452ms | 100% |
| **Mangas List** | 802ms | 1,298ms | 2,145ms | 100% |
| **Public Lists** | 283ms | 325ms | 398ms | 100% |

#### Análisis del Cold Start

> **⚠️ Cold Start Identificado**: Los servicios `Auth Health` y `List Health` muestran latencias máximas de ~22 segundos en el primer request, lo cual corresponde al **cold start** característico del tier gratuito de Render.

**Evidencia:**
- Request 1/5 de Auth Health: **22,439ms** (cold start - servicio dormido)
- Request 2/5 de Auth Health: **176ms** (servicio ya activo)

Esto confirma que los servicios entran en estado "dormido" tras ~15 minutos de inactividad en el plan gratuito. Una vez "calentado", la latencia baja a ~200ms.

### 6.3 Prueba de Carga con Script Python

![Latencia](docs/captures/SSH5/latencia.png)

### 6.4 Prueba de Estrés con Locust

Se realizo prueba de estrés con locust para verificar el rendimiento del sistema.

Se confirma que hay algunos errores frente a mucho estrés, debido a plan gratuito de render, sin embargo el sistema sigue funcionando correctamente, el usuario puede continuar su actividad normalmente, debido a que las peticiones son manejadas correctamente, al repetirse si fallan.

![Locust](docs/captures/SSH5/locustest.png)

### 6.5 Resultados de las Pruebas

| Prueba | Resultado | Observaciones |
|--------|-----------|---------------|
| **Latencia (p50)** | ~200ms | Aceptable para aplicación web |
| **Latencia (p95)** | ~500ms | Cold starts afectan |
| **Throughput** | ~40 req/s | Limitado por tier gratuito |


### 6.6 Conclusiones de Rendimiento

1. **✅ El tier gratuito de Render es adecuado** para proyectos de demostración, portfolios y desarrollo con la comprensión de sus limitaciones

2. **⏱️ Cold Starts son el principal factor de latencia**: Los servicios entran en estado "dormido" tras ~15 minutos de inactividad. El primer request puede tomar **hasta 22 segundos** mientras el contenedor se reinicia. Esto es **solucionable** con upgrade a plan de pago

3. **📊 Una vez "calentado" el rendimiento es excelente**: Latencias de 150-400ms son totalmente aceptables para una aplicación web moderna

4. **🛡️ Resiliencia comprobada**: A pesar de errores bajo estrés extremo, el sistema se recupera automáticamente y el frontend implementa reintentos

5. **🔄 La arquitectura de microservicios funciona**: Cada servicio puede escalarse y reiniciarse independientemente sin afectar a los demás

---

## 📎 Anexos

### Anexo A:

![Funcionamiento General](docs/captures/SSH5/navegacion.gif)

![Subida Colaborativa](docs/captures/SSH5/Upload.gif)



## 📚 Referencias

- [Render Documentation](https://render.com/docs)
- [Render Blueprints](https://render.com/docs/infrastructure-as-code)
- [GitHub Actions](https://docs.github.com/en/actions)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Autor**: Julio Rubio  
**Fecha**: Enero 2026  
**Asignatura**: Cloud Computing
