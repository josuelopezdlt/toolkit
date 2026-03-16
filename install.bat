@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
echo.
echo ══════════════════════════════════════════════
echo    Instalador — zstd_project
echo ══════════════════════════════════════════════
echo.

:: ── 1. Verificar Python ───────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en el PATH.
    echo.
    echo  Opciones:
    echo    A) Descarga Python desde https://python.org/downloads
    echo       y marca "Add Python to PATH" al instalar.
    echo    B) Si ya lo tienes instalado, agrega su carpeta al PATH manualmente:
    echo       Configuracion del sistema ^> Variables de entorno ^> PATH
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] %PYVER% encontrado.

:: ── 2. Agregar Python al PATH del usuario (persistente) ──
for /f "tokens=*" %%p in ('python -c "import sys, os; print(os.path.dirname(sys.executable))"') do set PYDIR=%%p
for /f "tokens=*" %%p in ('python -c "import sys, os; print(os.path.join(os.path.dirname(sys.executable), \"Scripts\"))"') do set PYSCRIPTS=%%p

:: Leer PATH actual del usuario
for /f "skip=2 tokens=3*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set CURRENT_PATH=%%a %%b

echo !CURRENT_PATH! | findstr /i "%PYDIR%" >nul
if errorlevel 1 (
    setx PATH "%PYDIR%;%PYSCRIPTS%;%CURRENT_PATH%" >nul
    echo [OK] Python agregado al PATH del usuario permanentemente.
) else (
    echo [OK] Python ya estaba en el PATH del usuario.
)

:: ── 3. Instalar dependencias ──────────────────
echo.
echo  Instalando dependencias...
python -m pip install --upgrade pip --quiet
python -m pip install -r "%~dp0requirements.txt"

if errorlevel 1 (
    echo.
    echo [ERROR] Fallo al instalar dependencias.
    pause
    exit /b 1
)

echo.
echo ══════════════════════════════════════════════
echo    Listo. Ejecuta el script con:
echo    python zstd_project.py
echo ══════════════════════════════════════════════
echo.
pause
