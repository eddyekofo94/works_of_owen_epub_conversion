"""
Zero-dependency progress display for the Owen Works pipeline.

Provides:
  progress_bar()   — build a \r-based bar string
  SequentialMode  — \r progress for sequential extract/render
  ParallelTracker — shared-dict progress for multiprocessing workers
"""

from __future__ import annotations

import re
import sys
import threading
import time


def progress_bar(current: int, total: int, prefix: str = "", width: int = 30) -> str:
    """Return a `\\r`-based progress bar string."""
    if total <= 0:
        return ""
    fraction = current / total
    filled = int(width * fraction)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(fraction * 100)
    return f"\r{prefix} [{bar}] {current}/{total} ({pct}%)"


def _is_tty() -> bool:
    return sys.stdout.isatty()


# ---------------------------------------------------------------------------
# Sequential mode — direct \r output (used by extract.py / render.py)
# ---------------------------------------------------------------------------

_DEFAULT_REFRESH_S = 0.08


class SequentialMode:
    """Print `\\r`-based progress to stdout (tty only)."""

    def __init__(self, total: int = 0, prefix: str = ""):
        self.total = total
        self.current = 0
        self.prefix = prefix
        self._last = 0.0

    def update(self, current: int | None = None, total: int | None = None) -> None:
        if not _is_tty():
            return
        now = time.time()
        if now - self._last < _DEFAULT_REFRESH_S:
            return
        self._last = now
        if current is not None:
            self.current = current
        if total is not None:
            self.total = total
        if self.total > 0:
            sys.stdout.write(progress_bar(self.current, self.total, self.prefix))
            sys.stdout.flush()

    def done(self, final_message: str = "") -> None:
        if _is_tty():
            sys.stdout.write("\r\033[K")
            if final_message:
                sys.stdout.write(final_message)
            sys.stdout.flush()


# ---------------------------------------------------------------------------
# Spinner — startup placeholder before real progress begins
# ---------------------------------------------------------------------------

_SPINNER_CHARS = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


class Spinner:
    """Daemon-thread spinner for the startup gap.

    Call ``start()`` before the pipeline begins and ``stop()`` when
    the first progress update arrives (see ``spinner_wrap_callback``).
    """

    def __init__(self, message: str = "Loading"):
        self.message = message
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if not _is_tty():
            return
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, final_message: str = "") -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.3)
        if _is_tty():
            sys.stdout.write("\r\033[K")
            if final_message:
                sys.stdout.write(f"{final_message}\n")
            sys.stdout.flush()

    def _spin(self) -> None:
        i = 0
        while self._running:
            ch = _SPINNER_CHARS[i % len(_SPINNER_CHARS)]
            sys.stdout.write(f"\r{self.message} {ch}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1


def spinner_wrap_callback(callback) -> tuple[callable, Spinner]:
    """Wrap a progress callback with a spinner that stops on first update.

    Returns ``(wrapped_callback, spinner)``.  Start ``spinner`` before
    the pipeline, pass ``wrapped_callback`` as the progress callback.
    """
    spinner = Spinner("Working")
    _started = False

    def wrapped(current, total, label):
        nonlocal _started
        if not _started:
            spinner.stop()
            _started = True
        if callback:
            callback(current, total, label)

    return wrapped, spinner


# ---------------------------------------------------------------------------
# Parallel mode — shared dict that the main process polls
# ---------------------------------------------------------------------------

_STALE_S = 3.0


class ParallelTracker:
    """Worker-side interface: writes progress to a shared dict.

    The main process creates a ``multiprocessing.Manager().dict()``, passes
    a reference to each worker (via function args), and the worker wraps it
    with ``ParallelTracker``.
    """

    def __init__(self, shared: dict, vol_num: int):
        self.shared = shared
        self.vol_num = vol_num
        self._last = 0.0
        shared[vol_num] = {"current": 0, "total": 1, "label": ""}

    def update(self, current: int, total: int = 1, label: str = "") -> None:
        now = time.time()
        if now - self._last < _DEFAULT_REFRESH_S:
            return
        self._last = now
        self.shared[self.vol_num] = {
            "current": current,
            "total": total,
            "label": label,
        }

    def done(self) -> None:
        state = self.shared.get(self.vol_num, {})
        total = state.get("total", 1)
        self.shared[self.vol_num] = {
            "current": total,
            "total": total,
            "label": "done",
        }


def _status_short(label: str) -> str:
    """Shorten a progress label like '[render] Volume 3' to 'R3'."""
    m = re.search(r"Volume (\d+)", label or "")
    stage = "E" if "extract" in (label or "") else "R"
    return f"{stage}{m.group(1)}" if m else label


def draw_parallel_panel(progress_dict: dict, volumes: list[int]) -> None:
    """Print a single-line `\\r` status for all parallel volumes."""
    if not _is_tty():
        return
    parts = []
    all_done = True
    for v in volumes:
        state = progress_dict.get(v)
        if state is None:
            parts.append(f"[{v}] …")
            all_done = False
            continue
        cur = state.get("current", 0)
        tot = state.get("total", 0)
        lbl = _status_short(state.get("label", ""))
        if tot > 0 and cur >= tot:
            parts.append(f"[{v}] ✓")
        elif tot > 0:
            pct = int(100 * cur / tot)
            parts.append(f"[{v}] {lbl} {pct}%")
            all_done = False
        else:
            parts.append(f"[{v}] …")
            all_done = False
    if all_done:
        return
    sys.stdout.write(f"\r{'  '.join(parts)}")
    sys.stdout.flush()


def clear_parallel_panel() -> None:
    """Clear the single-line status bar."""
    if _is_tty():
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
