# personal — setup inicial

Herramientas personales de desarrollo. Funciona como **setup inicial** y punto de entrada (`/init`) en cualquier máquina nueva.

---

## Estructura

```
personal/
├── zstd_project.py      # Herramienta de compresión/backup (menú + CLI)
├── install.sh           # Setup inicial — macOS / Linux
├── install.bat          # Setup inicial — Windows
├── init.sh              # Arranque rápido — macOS / Linux
├── init.bat             # Arranque rápido — Windows
├── requirements.txt     # Dependencias Python
└── erp_conexion/        # Scripts de conexión a Perseo ERP (HFSQL)
```

---

## Instalación (primera vez)

### macOS / Linux
```bash
bash install.sh
```
El instalador:
1. Verifica Python 3
2. Crea un entorno virtual en `.venv`
3. Instala dependencias (`zstandard`)
4. Registra el alias `zstd` en `.zshrc` / `.bashrc`

### Windows
```bat
install.bat
```

---

## Uso diario

### Menú interactivo
```bash
./init.sh          # macOS / Linux
init.bat           # Windows
```
O con el alias registrado:
```bash
zstd
```

### CLI directo
```bash
./init.sh compress  <ruta>              # Comprimir directorio
./init.sh compress  <ruta> --level 9   # Nivel de compresión 1-22
./init.sh decompress <archivo.tar.zst> --output <destino>
./init.sh list       <archivo.tar.zst> --verbose
```

---

## Configuración

| Variable de entorno  | Descripción                                    | Default                    |
|----------------------|------------------------------------------------|----------------------------|
| `ZSTD_SOURCE_DIR`    | Directorio raíz de proyectos para backup masivo | `~/Documents/source`       |

Ejemplo:
```bash
export ZSTD_SOURCE_DIR=~/Projects
./init.sh
```

También puedes cambiar el directorio en tiempo de ejecución con la **opción 6** del menú interactivo.

---

## erp_conexion

Scripts para extraer datos del ERP Perseo vía ODBC (HFSQL).  
Requiere un archivo `.env` con las credenciales del servidor HFSQL:

```
HFSQL_SERVER=192.168.x.x
HFSQL_PORT=5588
HFSQL_DATABASE=nombre_db
HFSQL_USER=usuario
HFSQL_PASSWORD=contraseña
```

Instalación de dependencias:
```bash
cd erp_conexion
pip install -r requirements.txt
```

Flujo de trabajo:
1. `explorar_schema.py` — descubrir tablas y columnas (ejecutar una vez)
2. `consultar.py` — extraer ventas por periodo a Excel
