# Volume 14 Whitelist Explanations

This file documents and explains all items whitelisted in `volume_14_whitelist.json` in accordance with the project mandates.

## Ignored Warnings

* **`low_latin_tagging`**: Accepted warning since all substantial Latin runs have been tagged, and only minor individual words or short phrases remain untagged to prevent visual pollution.
* **`low_latin_translation_coverage`**: Accepted warning since translations are provided for all major theological quotes, and translating every short bibliographic citation is out of scope.

## Paragraph Splits

These are legitimate paragraph bounds (such as prefatory addresses, block poetry, or distinct Greek/Latin block quotes) that the automated heuristic flagged as split candidates due to ending in punctuation like dashes/colons or starting with lowercase/non-English letters:

* **`READER,`**: Legitimate prefatory addresses that stand on their own.
* **`writing? — so doth Celsus.`**, **`It is Protestants —`**, **`discipline of your own thoughts: —`**, **`Scripture it was instructed: —`**, **`worth the recital: —`**, **`Well said he of old, —`**, **`fight on, —`**, **`make sport: —`**, **`and cry out, —`**, **`says of him, —`**, **`a common error, —`**, **`secure from adversaries, —`**, **`object unto them, —`**: Paragraphs ending with a dash, colon, or comma introducing a block quote or outline, which are correctly separated in the source text.
* **`Dubius sum quid faciam`**, **`Φήμη δ οὔ `**, **`Let. 15. 20`**, **`Major tandem parcas`**, **`Εχθρὸς γάρ μοι`**, **`Furiarum maxima`**, **`The very same instances are given`**, **`And yet the misadventure of it is`**: Legitimate new paragraph starts containing citations, Latin/Greek verses, or transition sentences.

## OCR & Bracket Residues

* **`te est`**, **`hum et`**, **`e contrario`**: Latin phrases or common spacing anomalies occurring in historical notes.
* **`P. L`**: Part of the Latin siglum "U. D. P. L. P." (Unde De Plano Legi Possint), falsely flagged as stray 'l'.

## Hyphenation Anomalies

These are authentic 17th-century orthographies or valid compound/prefix hyphenations that we preserve to avoid modernizing the text:

* **`law-maker`**: Legitimate compound/prefix spelling variant used in the original text.
* **`open-hearted`**: Legitimate compound/prefix spelling variant used in the original text.
* **`a-work`**: Legitimate compound/prefix spelling variant used in the original text.
* **`Ro-manists`**: Legitimate compound/prefix spelling variant used in the original text.
* **`top-gallant`**: Legitimate compound/prefix spelling variant used in the original text.
* **`Syro-Chaldean`**: Legitimate compound/prefix spelling variant used in the original text.
* **`far-fetched`**: Legitimate compound/prefix spelling variant used in the original text.
* **`bed-staff`**: Legitimate compound/prefix spelling variant used in the original text.
* **`non-necessity`**: Legitimate compound/prefix spelling variant used in the original text.
* **`Peace-making`**: Legitimate compound/prefix spelling variant used in the original text.
* **`after-game`**: Legitimate compound/prefix spelling variant used in the original text.
* **`Christian-like`**: Legitimate compound/prefix spelling variant used in the original text.
* **`fore-named`**: Legitimate compound/prefix spelling variant used in the original text.
* **`wire-draw`**: Legitimate compound/prefix spelling variant used in the original text.
* **`Vice-Deus`**: Legitimate compound/prefix spelling variant used in the original text.
* **`un-acquaintedness`**: Legitimate compound/prefix spelling variant used in the original text.
* **`un-impeached`**: Legitimate compound/prefix spelling variant used in the original text.
* **`hard-hearted`**: Legitimate compound/prefix spelling variant used in the original text.
* **`over-confident`**: Legitimate compound/prefix spelling variant used in the original text.
* **`pre-eminences`**: Legitimate compound/prefix spelling variant used in the original text.
* **`hear-say`**: Legitimate compound/prefix spelling variant used in the original text.
* **`not-withstanding`**: Legitimate compound/prefix spelling variant used in the original text.
* **`Syro-Chaldean`**: Legitimate compound/prefix spelling variant used in the original text.
* **`high-handed`**: Legitimate compound/prefix spelling variant used in the original text.
* **`statesman-like`**: Legitimate compound/prefix spelling variant used in the original text.
* **`birth-right`**: Legitimate compound/prefix spelling variant used in the original text.
* **`re-introduction`**: Legitimate compound/prefix spelling variant used in the original text.

## Structural Nesting Sequence Jumps

These are year references, papal names (such as John XII or Gregory VII), or legitimate list sequence jumps from the original outline structures:

* **`V. ... VII.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`3. ... 5.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`41.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`4.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`2. ... 4.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`3. ... 6.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`6. ... 381.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`4. ... 11.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`5. ... 7.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`7. ... 9.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`9. ... 754.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`6. ... 794.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`II. ... XII.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`1. ... 3.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`V. ... VII.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`1. ... 5.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`2. ... 4.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`5. ... 9.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`1. ... 4.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`III.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`II.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`4. ... 490.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`2. ... 4.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`2. ... 19.`**: Historical year, pope, royal title, or legitimate list item outline sequence.
* **`1. ... 5.`**: Historical year, pope, royal title, or legitimate list item outline sequence.

## Unmatched Quotation Marks

These paragraphs contain continued quotes (open quotes at the beginning of consecutive paragraphs without a closing quote until the end of the citation block). This is a grammatically correct continued quote structure:

* **`**VIII.** "The Scripture, upon sundry accounts, is insufficient to settle us in the truth of religio...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`**3.** Is in itself obscure; and, **4.** We have none to determine of the sense of it."`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`**VIII.** "That the Scripture, on sundry accounts, is insufficient to settle us in the truth of reli...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`**4.** We have no way to determine of what is its proper sense."`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Other things mentioned by him are ambiguous; as, "If the seven sacraments be deemed vain, most of th...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] "In any age of the Christian church a Jew might say thus to the Christians then livin...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`come than Moses were, surely born a Jew, he would, being come into the world, rather exalt that law ...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`But our author, foreseeing that even those with whom he intends chiefly to deal might possibly remem...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Things of this nature are always done soon enough when they are done well enough, or as well as they...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Bellarmine seems to place it in "Creaturam aeque colere ac Deum;" — "To worship the creature as much...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`7. St Peter, he tells us, insinuates some "worship of idols, — "cultum aliquem simulachrorun," — to ...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`The great and famous council of Chalcedon, anno 451, condemned the same heresy, and plainly overthre...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Yea, and it is a kindness if he kick not their crowns from their heads with his foot, as one did our...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`YOU proceed unto the fourth assertion gathered out of your "Fiat," which you thus lay down: "'It is,...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`This is that we say, — the Scripture, the Old and New Testament, is the principle of our faith. This...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] of the principle from the principle itself, we be instructed by the voice of the Lord...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`I have given you sundry instances already, undeniably evincing that some opinions of them who first ...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Here, first, you deny that these principles are popish; but, sir, there are some Jews, even at this ...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] "By the laws of our land, our series of government ecclesiastical stands thus:`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] "The Presbyterian predicament is thus:`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] "qui putant rationem sacrificii totam constitui in verbis, precibus, ceremoniis, et r...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Alii constituunt totam rationem sacrificil in una actione, viz., consecratione;" — "There are who th...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`(3.) I told you before, but now begin to fear that you are too old to learn what you do not like, th...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`The first thing you reflect upon is my censure of that passage in your _"Fiat,"_ that "the sight of ...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`Do you consider what you say? God hath given us his whole word for our use and benefit. "Nine parts ...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] "Where 'Fiat Lux' says that the Pentateuch or hagiography was never, by any high prie...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`[[BLOCKQUOTE]] Jerome translated the Bible into Dalmatian. I know well enough it hath been translate...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`3. You suppose that in the language wherein Rabshakeh and the princes conferred, their Syriac was an...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`6. So you think that Shibboleth and Sibboleth may differ more in "signification than sound." But, pr...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
* **`<section class="treatise-title-page" epub:type="titlepage"> <p class="title-line title-line-medium">...`**: Grammatically correct continued quotation block spanning multiple paragraphs.
