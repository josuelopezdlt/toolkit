"""
claude_quota.py
===============
Tracker para la cuota de uso de Claude (ventana de 5 horas).

Registra cuando se reinicia la cuota y muestra el tiempo restante
con una barra de progreso visual.

Estado persistido en ~/.config/toolkit/claude_quota.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

QUOTA_WINDOW = timedelta(hours=5)
STATE_DIR = Path.home() / ".config" / "toolkit"
STATE_FILE = STATE_DIR / "claude_quota.json"

BAR_WIDTH = 40
BAR_FULL = "\u2588"
BAR_EMPTY = "\u2591"


def _load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def _save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def _format_duration(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        return "0m"
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    if minutes > 0:
        return f"{minutes}m {seconds:02d}s"
    return f"{seconds}s"


def _progress_bar(fraction: float) -> str:
    filled = int(BAR_WIDTH * fraction)
    empty = BAR_WIDTH - filled
    return f"{BAR_FULL * filled}{BAR_EMPTY * empty}"


def cmd_reset(_args: argparse.Namespace) -> int:
    """Marca el inicio de una nueva ventana de 5 horas."""
    state = _load_state()
    now = _now()

    # Guardar en historial
    history: list[dict] = state.get("history", [])
    if "reset_at" in state:
        history.append({"reset_at": state["reset_at"]})
        # Mantener solo ultimas 20 entradas
        history = history[-20:]

    state["reset_at"] = now.isoformat()
    state["history"] = history
    _save_state(state)

    expires = now + QUOTA_WINDOW
    local_expires = expires.astimezone()
    print()
    print("  \u2705 Cuota reiniciada")
    print(f"  Inicio:     {now.astimezone():%Y-%m-%d %H:%M}")
    print(f"  Expira:     {local_expires:%Y-%m-%d %H:%M}")
    print(f"  Disponible: {_format_duration(QUOTA_WINDOW)}")
    print()
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    """Muestra el tiempo restante de la cuota actual."""
    state = _load_state()

    if "reset_at" not in state:
        print()
        print("  \u26a0\ufe0f  No hay cuota registrada.")
        print("  Usa 'claude reset' para marcar el inicio de tu ventana.")
        print()
        return 1

    reset_at = _parse_ts(state["reset_at"])
    now = _now()
    elapsed = now - reset_at
    remaining = QUOTA_WINDOW - elapsed

    if remaining.total_seconds() <= 0:
        # Cuota ya expiro
        print()
        print("  \u2705 Tu cuota ya se renovo!")
        print(f"  Expiro hace: {_format_duration(-remaining)}")
        print("  Usa 'claude reset' cuando inicies una nueva sesion.")
        print()
        return 0

    fraction_used = elapsed.total_seconds() / QUOTA_WINDOW.total_seconds()
    fraction_remaining = 1.0 - fraction_used
    pct = int(fraction_remaining * 100)

    local_reset = reset_at.astimezone()
    local_expires = (reset_at + QUOTA_WINDOW).astimezone()

    print()
    print("  \u23f3 Claude — Cuota de uso")
    print("  " + "\u2500" * 44)
    print(f"  Inicio:     {local_reset:%Y-%m-%d %H:%M}")
    print(f"  Expira:     {local_expires:%Y-%m-%d %H:%M}")
    print()
    print(f"  Restante:   {_format_duration(remaining)}  ({pct}%)")
    print(f"  [{_progress_bar(fraction_remaining)}]")
    print()

    # Alerta si queda poco
    if remaining < timedelta(minutes=30):
        print("  \u26a0\ufe0f  Menos de 30 minutos restantes!")
        print()
    elif remaining < timedelta(hours=1):
        print("  \U0001f4a1 Menos de 1 hora restante.")
        print()

    return 0


def cmd_history(_args: argparse.Namespace) -> int:
    """Muestra el historial de resets."""
    state = _load_state()
    history: list[dict] = state.get("history", [])

    current = state.get("reset_at")
    if not current and not history:
        print()
        print("  Sin historial registrado.")
        print()
        return 0

    print()
    print("  \U0001f4cb Historial de cuotas")
    print("  " + "\u2500" * 44)

    if current:
        reset_at = _parse_ts(current)
        local_t = reset_at.astimezone()
        print(f"  \u25b6 {local_t:%Y-%m-%d %H:%M}  (actual)")

    for entry in reversed(history[-10:]):
        t = _parse_ts(entry["reset_at"]).astimezone()
        print(f"    {t:%Y-%m-%d %H:%M}")

    print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tracker de cuota de uso de Claude (ventana de 5h)",
    )
    sub = parser.add_subparsers(dest="action")

    sub.add_parser("status", help="Mostrar tiempo restante")
    sub.add_parser("reset", help="Marcar inicio de nueva ventana")
    sub.add_parser("history", help="Ver historial de resets")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.action or args.action == "status":
        return cmd_status(args)
    if args.action == "reset":
        return cmd_reset(args)
    if args.action == "history":
        return cmd_history(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
