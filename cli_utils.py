"""
Minimal ANSI color helpers for CLI output.

Zero dependencies. All modern terminals support these escape codes.
"""

from __future__ import annotations

import sys


def _supports_color() -> bool:
    return sys.stdout.isatty()


def green(text: str) -> str:
    return f"\033[92m{text}\033[0m" if _supports_color() else text


def red(text: str) -> str:
    return f"\033[91m{text}\033[0m" if _supports_color() else text


def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m" if _supports_color() else text


def cyan(text: str) -> str:
    return f"\033[96m{text}\033[0m" if _supports_color() else text


def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m" if _supports_color() else text


def dim(text: str) -> str:
    return f"\033[2m{text}\033[0m" if _supports_color() else text


def status_icon(ok: bool) -> str:
    """Return ✓ in green or ✗ in red."""
    return green("✓") if ok else red("✗")
