# Volume 2 Code Hardening Report

**Date:** 2026-05-19  
**Status:** IMPLEMENTED (AWAITING VALIDATION)

## Scope

This pass reviewed the shared conversion seams before beginning Volume 2, especially:

- `shared.py`
- `extract.py`
- `render.py`
- `volumes/v1/convert.py`

The goal was not to add new extraction behavior, but to reduce brittle coupling so small Volume 2 overrides do not accidentally disturb generic pipeline behavior.

## Code Qualities Observed

- The project now has a strong two-stage contract: `extract.py` writes JSON, `render.py` consumes it.
- Volume-specific fixes are already isolated through `OVERRIDES`, which is the right architecture for the remaining 15 volumes.
- The holistic paragraph healing remains centralized in `reconstruct_paragraphs()` and is still the correct guard against page-boundary fragmentation.
- The current audit and regression suite is valuable: it catches recurring failure classes rather than only checking one final EPUB.

## Improvements Made

### 1. Recursive Volume Config Merge

Before this pass, both `extract_volume()` and `render_volume()` used a shallow merge:

```python
config = {**VOLUME_CONFIG.get(vol_num, {}), **overrides}
```

That is brittle because adding one nested override, such as `regex_replacements`, replaces the whole shared nested map. For V2 and later volumes, that could silently drop defaults.

I added `merge_volume_config()` in `shared.py` and routed both Stage 1 and Stage 2 through it. Nested maps now compose predictably while lists and scalar values still override normally.

### 2. Shared Per-Volume CLI

The V1 script carried duplicated argparse and stage-running boilerplate. I moved that behavior into `shared.run_volume_cli()`.

This keeps future `volumes/vN/convert.py` files small and harder to copy incorrectly.

### 3. Clean Volume 2 Entrypoint

I added `volumes/v2/convert.py` with an empty `OVERRIDES = {}`.

This gives Volume 2 the preferred pipeline entrypoint without importing any V1-only catechism/title-page logic. Future V2 fixes can be added locally only when needed.

### 4. Config Regression Tests

I added `tests/test_config_hardening.py` to ensure:

- nested override maps are deep-merged;
- shared `VOLUME_CONFIG` defaults are not mutated by a per-volume override.

## Validation

- Python compile check passed for:
  - `shared.py`
  - `extract.py`
  - `render.py`
  - `volumes/v1/convert.py`
  - `volumes/v2/convert.py`
- Focused config and footnote tests: `3 passed`
- Full focused regression set: `29 passed`
- V1 render-only rebuild completed successfully.
- V1 EPUB audit: `0 errors`, `1 warning` (`repeated_phrases`)
- V1 bug regression audit: `PASS`
- V1 text-integrity audit remained at `0.9945` coverage and improved paragraph counts:
  - possible split candidates: `106`
  - inline structural marker candidates: `0`
  - missing enumerator markers: `0`

## Remaining Risks

- `extract.py` still imports many render constants and helpers. This is stable enough for V2, but the long-term cleaner architecture would be a small `pipeline_patterns.py` or `pipeline_common.py` for shared regexes and text utilities.
- `render.py` is still a large module. It is workable, but later cleanup should split EPUB assembly, structural Markdown rendering, and title-page polishing into separate modules.
- Volume-specific hooks remain dict-based. The new merge helper reduces risk, but a typed config object would be cleaner if the hook surface grows.

## Recommendation For Volume 2

Start V2 with the new command:

```bash
.venv/bin/python3 volumes/v2/convert.py
```

Keep `OVERRIDES` empty until the first concrete V2-only issue appears. If a fix is generic, put it in `extract.py`, `render.py`, or `shared.py`; if it is source-specific or volume-specific, put it in `volumes/v2/convert.py`.
