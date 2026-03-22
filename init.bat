@echo off
:: init.bat — Punto de entrada principal (Windows)
:: Activa el entorno virtual e inicia zstd_project.
:: Uso:  init.bat [argumentos para zstd_project.py]

set SCRIPT_DIR=%~dp0
set VENV_PYTHON=%SCRIPT_DIR%.venv\Scripts\python.exe

:: ── Verificar que el entorno esté instalado ──
if not exist "%VENV_PYTHON%" (
    echo.
    echo   [!] Entorno virtual no encontrado.
    echo   Ejecuta primero:  install.bat
    echo.
    pause
    exit /b 1
)

:: ── Lanzar la herramienta ─────────────────────
"%VENV_PYTHON%" "%SCRIPT_DIR%zstd_project.py" %*
