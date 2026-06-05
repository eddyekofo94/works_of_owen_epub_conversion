## 1
v1
Dr. Isaac‡ Watts who succeeded (1702):
Status: IMPLEMENTED (AWAITING VALIDATION)
Correction:
1. Changed biography key "Isaac" to "Johannes Isaac" in scripts/biography_db.py to avoid false matches on "Isaac Watts" or the biblical patriarch "Isaac".
2. Added text replacement in volumes/v1/convert.py to specify the missing name: "Dr. Isaac Watts, who succeeded Dr. Isaac Chauncy (1702) to the charge".

## 2
"Believe in the Lord your God, so shall ye be established; believe his prophets, so shall ye prosper.‡"
Status: IMPLEMENTED (AWAITING VALIDATION)
Correction:
1. Made the biography scanner case-sensitive in render.py and scripts/epub_pages.py (removed the re.I flag) so that the lowercase verb "prosper" does not trigger a false match on the theologian "Prosper of Aquitaine".
