#!/usr/bin/env python3
"""
Legacy CLI wrapper for the modular Owen Works converter.

The active pipeline lives in:
    extract.py  - Stage 1: PDF -> JSON intermediate
    render.py   - Stage 2: JSON intermediate -> EPUB3

Prefer per-volume scripts such as volumes/v1/convert.py when volume-specific
OVERRIDES are needed. This wrapper intentionally remains generic so older
commands keep working without carrying a second copy of converter logic.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from extract import (
    clean_text,
    extract_volume,
    get_merged_page_text,
    get_pages_text,
    reconstruct_paragraphs,
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


def process_owen_volume(
    vol_num: int,
    *,
    extract_only: bool = False,
    render_only: bool = False,
) -> bool:
    """Run the generic two-stage pipeline for one Owen volume."""
    if vol_num not in OWEN_VOLUME_RANGE:
        raise ValueError(f"Volume must be between 1 and 16, got {vol_num}")

    if extract_only and render_only:
        raise ValueError("Cannot use both extract_only and render_only")

    if not render_only:
        print(f"=== Volume {vol_num}: Stage 1 - Extract ===")
        extract_volume(vol_num)

    if not extract_only:
        print(f"=== Volume {vol_num}: Stage 2 - Render ===")
        render_volume(vol_num)

    print(f"=== Volume {vol_num}: Done ===")
    return True


def process_all_volumes(
    *,
    extract_only: bool = False,
    render_only: bool = False,
) -> None:
    """Process all 16 Owen volumes through the generic legacy wrapper."""
    for vol_num in OWEN_VOLUME_RANGE:
        process_owen_volume(
            vol_num,
            extract_only=extract_only,
            render_only=render_only,
        )


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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.extract_only and args.render_only:
        print("Error: cannot use both --extract-only and --render-only", file=sys.stderr)
        return 2

    if args.hebrews:
        print("Hebrews pipeline is intentionally out of scope for this converter.")
        return 1

    volumes = [1] if args.test else args.volumes

    try:
        if volumes:
            for vol_num in volumes:
                process_owen_volume(
                    vol_num,
                    extract_only=args.extract_only,
                    render_only=args.render_only,
                )
        else:
            process_all_volumes(
                extract_only=args.extract_only,
                render_only=args.render_only,
            )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
