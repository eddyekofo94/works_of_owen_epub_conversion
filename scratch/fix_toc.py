import sys
import re

with open('volumes/v16/convert.py', 'r') as f:
    content = f.read()

replacement = """
    # Fix TOC Greek/Hebrew artifacts and typos
    for fm in intermediate.get('front_matter', []):
        html = fm.get('html', '')
        html = html.replace('aujto&gt;grafa', '<span lang="el">αὐτόγραφα</span>')
        html = html.replace('zeopneustoi', '<span lang="el">θεόπνευστοι</span>')
        html = html.replace('ejk tw~n ajduna&gt;twn', '<span lang="el">ἐκ τῶν ἀδυνάτων</span>')
        html = html.replace('zhtei~n to&lt;n Ku&gt;rion eji a]rage yhlafh&gt;seian aujto&lt;n kai&lt;', '<span lang="el">ζητεῖν τὸν Κύριον εἰ ἄραγε ψηλαφήσειαν αὐτὸν καὶ</span>')
        html = html.replace('to&lt; loipo&lt;n ou+n', '<span lang="el">τὸ λοιπὸν οὖν</span>')
        html = html.replace('bytik]W yriq]', '<span lang="he" dir="rtl">קְרִי וּכְתִיב</span>')
        html = html.replace('putty of the originals', 'purity of the originals')
        fm['html'] = html

    return intermediate
"""

content = content.replace('return intermediate', replacement)

with open('volumes/v16/convert.py', 'w') as f:
    f.write(content)
