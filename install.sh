#!/usr/bin/env bash
# install.sh — macOS/Linux
set -e

echo ""
echo "══════════════════════════════════════════════"
echo "   Instalador — zstd_project"
echo "══════════════════════════════════════════════"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── 1. Verificar Python ───────────────────────
if command -v python3 &>/dev/null; then
    PYTHON=python3
    echo "[OK] $(python3 --version) encontrado."
elif command -v python &>/dev/null; then
    PYTHON=python
    echo "[OK] $(python --version) encontrado."
else
    echo "[ERROR] Python no encontrado."
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Instala con Homebrew:"
        echo "    brew install python"
        echo ""
        echo "  O descarga desde: https://python.org/downloads"
    else
        echo "  Instala con tu gestor de paquetes:"
        echo "    sudo apt install python3   # Debian/Ubuntu"
        echo "    sudo dnf install python3   # Fedora"
    fi
    echo ""
    exit 1
fi

# ── 2. Agregar Python al PATH (si no está) ────
PYDIR="$(dirname "$($PYTHON -c 'import sys; print(sys.executable)')")"
SHELL_RC=""

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: detectar shell
    if [[ "$SHELL" == */zsh ]]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bash_profile"
    fi
else
    SHELL_RC="$HOME/.bashrc"
fi

if [[ ":$PATH:" != *":$PYDIR:"* ]]; then
    echo "export PATH=\"$PYDIR:\$PATH\"" >> "$SHELL_RC"
    echo "[OK] Python agregado al PATH en $SHELL_RC"
    echo "     Recarga con: source $SHELL_RC"
else
    echo "[OK] Python ya estaba en el PATH."
fi

# ── 3. Instalar dependencias ──────────────────
echo ""
echo "  Instalando dependencias..."
$PYTHON -m pip install --upgrade pip --quiet
$PYTHON -m pip install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "══════════════════════════════════════════════"
echo "   Listo. Ejecuta el script con:"
echo "   python3 zstd_project.py"
echo "══════════════════════════════════════════════"
echo ""
