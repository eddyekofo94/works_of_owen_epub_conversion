import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
translation_db_path = os.path.join(_ROOT, 'translation_db.py')

REMAINING_V12_TRANSLATIONS = {
    "v12_fn107": (
        "<b>Modern Citation:</b> Aristotle, <i>Nicomachean Ethics</i>, Book 10, Chapter 2, 1172b36.<br/>"
        "<b>Translation:</b> &ldquo;For what seems true to all, this we assert to be true; and he who destroys this belief will not have anything more trustworthy to offer.&rdquo;"
    ),
    "v12_fn109": (
        "<b>Modern Citation:</b> Gregory Nazianzen, <i>Oration 30</i> (Theological Oration 4), Section 3.<br/>"
        "<b>Translation:</b> &ldquo;Truth lies not in the sound of the voice, but in the mind.&rdquo;"
    ),
    "v12_fn110": (
        "<b>Modern Citation:</b> Arius, cited in Sozomen, <i>Ecclesiastical History</i>, Book 1, Chapter 14, p. 215; Theodoret, <i>Ecclesiastical History</i>, Book 1, Chapter 2, p. 8; Socrates Scholasticus, <i>Ecclesiastical History</i>, Book 1, Chapter 3. Nestorius, <i>ibid.</i><br/>"
        "<b>Translation Summary:</b> Arius said: &ldquo;There was a time when he [the Son] was not; he was made out of things that were not.&rdquo; Nestorius said: &ldquo;I do not say that the Word of God is united to a man, but I say that there are two substances [hypostases] and a division. And if he called Christ both man and God, it was not as we do, but by relation and association, on account of their supreme friendship.&rdquo;"
    ),
    "v12_fn135": (
        "<b>Modern Citation:</b> Philo Judaeus, <i>Allegorical Interpretation</i>, Book 2, Section 1.<br/>"
        "<b>Translation:</b> &ldquo;Hear a most true word from God who knows: 'God is not in a place, for He is not contained, but He contains the universe. But that which is created must necessarily be contained in a place, and does not contain.'&rdquo;"
    ),
    "v12_fn171": (
        "<b>Modern Citation:</b> Homer, <i>Iliad</i>, Book 16 [Rhapsody 16], lines 431–434.<br/>"
        "<b>Translation:</b> &ldquo;And when he saw them, the son of crooked-counseling Cronos took pity, and spoke to Hera: 'Ah, woe is me, that it is fated for Sarpedon, dearest of men to me, to be subdued by Patroclus, son of Menoetius.'&rdquo;"
    ),
    "v12_fn172": (
        "<b>Modern Citation:</b> Homer, <i>Iliad</i>, Book 5 [Rhapsody 5], lines 859–864.<br/>"
        "<b>Translation:</b> &ldquo;Then brazen Ares bellowed as loud as nine thousand men or ten thousand cry out in battle... and he sat down weeping, and showed the immortal blood flowing from the wound, and lamented.&rdquo;"
    ),
    "v12_fn175": (
        "<b>Modern Citation:</b> Aeschylus, <i>Suppliant Women</i>, lines 1057–1058; Hippocrates, <i>On Principles</i> [De Principiis / De Carnibus]; Epicharmus, Fragment, cited in Stobaeus, <i>Excerpta</i>, p. 117.<br/>"
        "<b>Translation:</b> &ldquo;How can I behold the divine mind, a bottomless view?&rdquo; (Aeschylus) / &ldquo;It seems to me that what we call heat is immortal and understands all things, and sees, hears, and knows both what is present and what is to come.&rdquo; (Hippocrates) / &ldquo;Nothing escapes the divine; he himself is our overseer.&rdquo; (Epicharmus) / &ldquo;From whom not a single person is hidden, either doing or about to do anything, or having done it long ago; but being present everywhere, he necessarily knows all things.&rdquo; (Stobaeus)"
    ),
    "v12_fn261": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;You said a little above that the Lord Jesus is by nature a man; does he also have a divine nature? — By no means; for that is repugnant not only to sound reason, but also to the holy Scriptures.&rdquo;"
    )
}

with open(translation_db_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate FOOTNOTE_TRANSLATIONS = {
target_str = "FOOTNOTE_TRANSLATIONS = {"
idx = content.find(target_str)
if idx == -1:
    print("Error: FOOTNOTE_TRANSLATIONS dictionary start not found!")
    sys.exit(1)

insert_idx = idx + len(target_str)

# Build string to insert
entries_str = "\n"
for key, val in sorted(REMAINING_V12_TRANSLATIONS.items()):
    val_escaped = val.replace('"', '\\"')
    entries_str += f'    "{key}": (\n        "{val_escaped}"\n    ),\n'

new_content = content[:insert_idx] + entries_str + content[insert_idx:]

with open(translation_db_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully added remaining 8 Volume 12 translations to translation_db.py!")
