# Project Guidelines

## Code Style
- Mantener cada utilidad pequena, autocontenida y facil de ejecutar desde CLI.
- Preferir Python estandar y dependencias minimas; este repo no es para infraestructura compartida ni orquestacion compleja.
- Conservar una interfaz clara en `toolkit.py` y delegar la logica especifica a modulos standalone.
- No hardcodear secretos ni rutas del entorno; usar variables de entorno cuando aplique.

## Architecture
- `toolkit.py` es el entry point del CLI y del menu interactivo.
- `zstd_project.py` implementa la utilidad principal actual y se invoca a traves del subcomando `zstd`.
- El setup del entorno, bootstrap de maquina, tokens y tareas operativas viven en `infra`, no en este repo.

## Build and Test
- En Mac/Linux usar `bash run.sh`; en Windows usar `run.bat`.
- Ambos scripts crean `.venv` si hace falta, instalan dependencias y ejecutan el CLI.
- Ejecucion directa: `python toolkit.py [comando]` con el entorno activo.
- No hay suite de tests documentada; validar cambios ejecutando el comando o flujo interactivo afectado.

## Conventions
- Mantener compatibilidad del passthrough `toolkit.py zstd ...`; no romper la superficie CLI existente sin actualizar ayuda y README.
- `ZSTD_SOURCE_DIR` controla el directorio raiz para operaciones masivas; preferirlo sobre rutas embebidas.
- Revisar con cuidado que archivos quedan incluidos en archivos comprimidos antes de cambiar exclusiones por defecto.

## Key References
- `README.md` para uso rapido y comandos disponibles.
- `CLAUDE.md` para arquitectura y alcance del repo.
- `toolkit.py` y `zstd_project.py` como ejemplos del patron de utilidades standalone.