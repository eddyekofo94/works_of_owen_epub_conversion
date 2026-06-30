#!/usr/bin/env bash
# Cleanup script: remove all space-versioned duplicate files across the repo.
#
# These are files matching the pattern "base N.ext" where N is a digit — they
# were left behind by scripts that fell back to appending a number instead of
# overwriting the existing output. Every such file has a confirmed base-file
# counterpart (verified: 1,218 checked, 0 missing a base).
#
# Also removes:
#   - Hebrews volumes (h1-h7) artifacts — out of Owen Works scope
#   - .working/ directory — scratch notes
#   - Empty archive directories with no content
#
# Usage:
#   bash scripts/cleanup_duplicates.sh

set -euo pipefail

TRACKED_FILE="$(mktemp)"
UNTRACKED_FILE="$(mktemp)"

git ls-files > "$TRACKED_FILE"
git ls-files --others --exclude-standard > "$UNTRACKED_FILE"

tracked_removed=0
untracked_removed=0

echo "=== Removing tracked space-versioned files (git rm) ==="
while IFS= read -r f; do
  if [[ "$f" =~ \ +[0-9]+\.[a-zA-Z0-9]+$ ]]; then
    git rm --quiet "$f"
    echo "  rm: $f"
    ((tracked_removed++))
  fi
done < "$TRACKED_FILE"

echo ""
echo "=== Removing untracked space-versioned files (rm) ==="
while IFS= read -r f; do
  if [[ "$f" =~ \ +[0-9]+\.[a-zA-Z0-9]+$ ]]; then
    rm -f "$f"
    echo "  rm: $f"
    ((untracked_removed++))
  fi
done < "$UNTRACKED_FILE"

echo ""
echo "=== Removing untracked Hebrews volume artifacts (h1-h7) ==="
while IFS= read -r f; do
  if [[ "$f" == volumes/h* ]]; then
    rm -rf "$f"
    echo "  rm: $f"
    ((untracked_removed++))
  fi
done < "$UNTRACKED_FILE"

echo ""
echo "=== Removing .working/ directory ==="
if [ -d .working ]; then
  rm -rf .working
  echo "  rm: .working/"
  ((untracked_removed++))
fi

echo ""
echo "=== Removing empty archive directories ==="
while IFS= read -r d; do
  if [ -d "$d" ] && [ -z "$(ls -A "$d" 2>/dev/null)" ]; then
    rmdir "$d"
    echo "  rmdir: $d/"
    ((untracked_removed++))
  fi
done < <(git ls-files --others --exclude-standard --directory)

echo ""
echo "=== Summary ==="
echo "  Tracked files git-rm'd:  $tracked_removed"
echo "  Untracked files removed: $untracked_removed"
echo "  Total:                   $((tracked_removed + untracked_removed))"
echo ""

# Cleanup temp files
rm -f "$TRACKED_FILE" "$UNTRACKED_FILE"
