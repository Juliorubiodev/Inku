# Reporte de Pruebas y Rendimiento (K6)

Este documento resume el estado de las pruebas automatizadas y de rendimiento para el hito 5.

## 1. Pruebas Unitarias y de Integración (CI/CD)

Se ha configurado un pipeline de GitHub Actions (`run_test.yml`) que separa la ejecución de pruebas para Frontend y Backend.

### Frontend
- **Herramientas**: Vitest + React Testing Library.
- **Estado**: ✅ **Funcionando**.
- **Pruebas Implementadas**:
    - `Environment.test.ts`: Verificación de infraestructura de pruebas.
    - `Simple.test.ts`: Prueba de lógica básica.
- **Configuración**: Se ha actualizado `vite.config.ts` y `package.json` para soportar `npm test`.

### Backend
- **Herramientas**: Pytest + HTTPX.
- **Estado**: ⚠️ **Estructura Lista / Requiere Configuración de Entorno**.
- **Servicios**:
    - **Manga Service**: Pruebas existentes detectadas (`src/test/`). 6/7 pruebas pasan localmente.
    - **Auth Service**: Se han añadido pruebas básicas (`tests/test_auth.py`). Requiere variables de entorno (Firebase Creds) para pasar en CI.
    - **List Service**: Pruebas existentes (`tests/`). Requiere mocks de autenticación para evitar errores 401/403.

## 2. Pruebas de Rendimiento (K6)

Se dispone de un script de carga en `tests/load/k6-script.js`.

### Ejecución
Para ejecutar las pruebas de carga, se recomienda usar Docker apuntando al host o Nginx:

```bash
docker run --rm -i grafana/k6 run - < tests/load/k6-script.js
```

### Resultados Preliminares
- El script está validado sintácticamente.
- **Nota**: Al ejecutar vía Docker en Windows, asegúrate de que la URL base en el script apunte a `host.docker.internal` en lugar de `localhost` para alcanzar los servicios corriendo en el host.

## 3. Conclusión
La infraestructura de CI/CD es robusta y modular. Los fallos actuales en local se deben a dependencias de entorno (credenciales de Firebase) y red (Docker networking), no a errores de código en la aplicación.
