#!/usr/bin/env python3
"""
Legacy CLI wrapper for the modular Owen Works converter.

The active pipeline lives in:
    extract.py  - Stage 1: PDF -> JSON intermediate
    render.py   - Stage 2: JSON intermediate -> EPUB3

Per-volume OVERRIDES from volumes/vN/convert.py are loaded automatically,
so this wrapper now respects the same volume-specific corrections as the
per-volume scripts.
"""

from __future__ import annotations

import argparse
import importlib
import io
import multiprocessing
import os
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli_utils import cyan, green

from shared import FONT_FAMILY_MAP, merge_volume_config

from extract import (
    clean_text,
    extract_volume,
    get_merged_page_text,
    get_pages_text,
    reconstruct_paragraphs,
)
from progress import (
    ParallelTracker,
    SequentialMode,
    Spinner,
    clear_parallel_panel,
    draw_parallel_panel,
    spinner_wrap_callback,
)
from render import force_polyglot_mapping, markdown_to_html, render_volume

# Compatibility surface for older tests/scripts that imported helpers from the
# monolithic converter before the Issue 91 module split.
__all__ = [
    "clean_text",
    "force_polyglot_mapping",
    "get_merged_page_text",
    "get_pages_text",
    "markdown_to_html",
    "process_all_volumes",
    "process_owen_volume",
    "reconstruct_paragraphs",
    "render_volume",
    "extract_volume",
]

OWEN_VOLUME_RANGE = range(1, 17)

_POLL_INTERVAL_S = 0.15


def _load_volume_overrides(vol_num: int) -> dict | None:
    """Import OVERRIDES from volumes/v{vol_num}/convert.py if it exists."""
    try:
        mod = importlib.import_module(f"volumes.v{vol_num}.convert")
        return getattr(mod, "OVERRIDES", None)
    except (ImportError, AttributeError):
        return None


def process_owen_volume(
    vol_num: int,
    *,
    extract_only: bool = False,
    render_only: bool = False,
    progress_callback=None,
) -> bool:
    """Run the generic two-stage pipeline for one Owen volume."""
    if vol_num not in OWEN_VOLUME_RANGE:
        raise ValueError(f"Volume must be between 1 and 16, got {vol_num}")

    if extract_only and render_only:
        raise ValueError("Cannot use both extract_only and render_only")

    overrides = _load_volume_overrides(vol_num)

    config = merge_volume_config(vol_num, overrides)
    body_font = config.get('body_font', 'unknown')
    internal_name = FONT_FAMILY_MAP.get(body_font, body_font)
    treatises = config.get('treatises', [])
    langs = config.get('secondary_languages')

    print(cyan(f'═══ Volume {vol_num} — config ═══'))
    print(f'  Title:      {config.get("title", "unknown")}')
    print(f'  Font:       {body_font} → "{internal_name}"')
    print(f'  Source:     {config.get("source_type", "unknown")}')
    print(f'  Treatises  ({len(treatises)}):')
    for i, t in enumerate(treatises, 1):
        print(f'    {i}. {t}')
    if langs:
        print(f'  Languages:  {", ".join(langs)}')
    print()

    if not render_only:
        print(cyan(f"=== Volume {vol_num}: Stage 1 - Extract ==="))
        _extract_cb, _extract_spin = spinner_wrap_callback(progress_callback)
        _extract_spin.message = f"Extracting Volume {vol_num}"
        _extract_spin.start()
        extract_volume(vol_num, overrides=overrides, progress_callback=_extract_cb)

    if not extract_only:
        print(cyan(f"=== Volume {vol_num}: Stage 2 - Render ==="))
        _render_cb, _render_spin = spinner_wrap_callback(progress_callback)
        _render_spin.message = f"Rendering Volume {vol_num}"
        _render_spin.start()
        render_volume(vol_num, overrides=overrides, progress_callback=_render_cb)

    print(green(f"=== Volume {vol_num}: Done ==="))
    return True


def process_all_volumes(
    *,
    extract_only: bool = False,
    render_only: bool = False,
    progress_callback=None,
) -> None:
    """Process all 16 Owen volumes through the generic legacy wrapper."""
    for vol_num in OWEN_VOLUME_RANGE:
        process_owen_volume(
            vol_num,
            extract_only=extract_only,
            render_only=render_only,
            progress_callback=progress_callback,
        )


def _make_seq_progress() -> callable:
    """Return a progress callback for sequential mode (\\r to terminal)."""
    seq = SequentialMode()

    def _cb(current, total, label):
        seq.prefix = label
        seq.update(current, total)
        if current >= total:
            seq.done(final_message=f"\r\033[K{label} {current}/{total} ✓\n")

    return _cb


def _render_worker(args: tuple) -> tuple[int, bool, str, str | None]:
    """Worker for parallel rendering: render one volume, capture output."""
    vol_num, extract_only, render_only, progress_dict = args
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    tracker = ParallelTracker(progress_dict, vol_num)
    try:

        def _cb(current, total, label):
            tracker.update(current, total, label)

        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            process_owen_volume(
                vol_num,
                extract_only=extract_only,
                render_only=render_only,
                progress_callback=_cb,
            )
        tracker.done()
        return vol_num, True, out_buf.getvalue(), None
    except Exception as exc:
        tracker.done()
        return vol_num, False, out_buf.getvalue(), str(exc)


def process_all_volumes_parallel(
    volumes: list[int],
    *,
    jobs: int = 4,
    extract_only: bool = False,
    render_only: bool = True,
) -> None:
    """Render volumes in parallel with output buffering.

    Defaults to render-only (safe from cached JSON). Extract-parallel is
    memory-heavy; if explicitly combined with --extract-only, jobs are
    capped at 2.
    """
    effective_jobs = max(1, min(jobs, os.cpu_count() or 4))
    if extract_only and not render_only:
        effective_jobs = min(effective_jobs, 2)

    print(green(f"Parallel mode: {len(volumes)} volume(s), {effective_jobs} worker(s)"))

    # Shared progress dict
    manager = multiprocessing.Manager()
    progress_dict = manager.dict()

    worker_args = [(v, extract_only, render_only, progress_dict) for v in volumes]
    pool = multiprocessing.Pool(effective_jobs)
    result_async = pool.map_async(_render_worker, worker_args)

    # Poll and draw progress panel while workers run
    try:
        while not result_async.ready():
            draw_parallel_panel(progress_dict, volumes)
            time.sleep(_POLL_INTERVAL_S)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        print("\nInterrupted.")
        return

    clear_parallel_panel()
    results = result_async.get()

    failed = []
    for vol_num, ok, output, err in sorted(results, key=lambda r: r[0]):
        sys.stdout.write(output)
        if not ok:
            print(f"\n{vol_num}: ERROR — {err}", file=sys.stderr)
            failed.append(vol_num)

    if failed:
        print(f"\nFailed volumes: {failed}", file=sys.stderr)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Legacy wrapper for the Owen Works extract/render pipeline",
    )
    parser.add_argument(
        "volumes",
        nargs="*",
        type=int,
        help="Volume numbers to process. Defaults to all 16 for legacy compatibility.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Process volume 1 only.",
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Run Stage 1 only (PDF -> JSON intermediate).",
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Run Stage 2 only (JSON intermediate -> EPUB3).",
    )
    parser.add_argument(
        "--hebrews",
        action="store_true",
        help="Reserved legacy flag; Hebrews commentary is intentionally out of scope.",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Render volumes in parallel (defaults to render-only, max 4 workers).",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=4,
        help="Max worker processes (capped at cpu_count; default 4).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all 16 volumes (overrides --test).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.extract_only and args.render_only:
        print("Error: cannot use both --extract-only and --render-only", file=sys.stderr)
        return 2

    if args.hebrews:
        print("Hebrews pipeline is intentionally out of scope for this converter.")
        return 1

    volumes = list(OWEN_VOLUME_RANGE) if args.all else ([1] if args.test else args.volumes)

    # Parallel path
    if args.parallel:
        extract_only = args.extract_only
        render_only = args.render_only
        # Default to render-only when neither flag is given (safe from cached JSON)
        if not extract_only and not render_only:
            render_only = True
            extract_only = False
        if extract_only:
            print("Warning: parallel extract is memory-heavy; capped to 2 workers.", file=sys.stderr)

        vols = volumes if volumes else list(OWEN_VOLUME_RANGE)
        try:
            process_all_volumes_parallel(
                vols,
                jobs=args.jobs,
                extract_only=extract_only,
                render_only=render_only,
            )
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    # Sequential path
    seq_progress = _make_seq_progress()
    try:
        if volumes:
            for vol_num in volumes:
                process_owen_volume(
                    vol_num,
                    extract_only=args.extract_only,
                    render_only=args.render_only,
                    progress_callback=seq_progress,
                )
        else:
            process_all_volumes(
                extract_only=args.extract_only,
                render_only=args.render_only,
                progress_callback=seq_progress,
            )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
