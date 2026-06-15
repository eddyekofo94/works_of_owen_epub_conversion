# Volume 7 Repair Plan — Healing Session

This repair plan checklist documents the quality healing steps taken to stabilize and validate Volume 7 (*The Grace and Duty of Being Spiritually Minded*).

## Quality Target
- Status: **PRISTINE** (Quality Need score < 20.0)
- Goal: Bring Need score to its optimal minimum and resolve all failing regression checks.

## Repair Checklist

- [x] **Git Branch Setup:** Switch to a dedicated healing branch `heal-v7` from `master`.
- [x] **Baseline Assessment:** Execute standard checks (`scripts/run_all_checks.py 7`) to identify issues.
  - *Result:* Audits pass cleanly (0 errors, 0 warnings, 99.8% coverage), but `test_no_unused_whitelist_entries` fails due to dead/stale whitelist exclusions.
- [x] **Clean Whitelist Exclusions:** Update `volume_7_whitelist.json` and `volume_7_whitelist.md` to remove unused items that are no longer triggering warnings:
  - Remove weak page exemptions for page 7 and page 24.
  - Remove dense source window loss exemption for page 59.
  - Remove structural marker exemption: `"whereas, 1. the law gives no strength against sin"`.
  - Remove paragraph split exemption: `"D.D. LONDON: 1688"`.
  - Remove unused ignored warnings: `weak_page_coverage`, `top_of_page_text_loss`, and `bottom_of_page_text_loss`.
- [x] **Regression Verification:** Run `scripts/run_all_checks.py 7` to rebuild, audit, and execute pytest.
  - *Result:* **PASS** (100% green pass rate).
- [x] **Final State Scoring:** Re-run the volume state report.
  - *Result:* Volume 7 is validated at **PRISTINE** status with a quality Need score of **19.6** (0 errors, 0 warnings, 0 splits, 0 unresolved citations).
