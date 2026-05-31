import re

with open('scratch/v1_toc_raw.html', 'r') as f:
    html = f.read()

# Fix CRISTOLOGIA
html = html.replace('CRISTOLOGIA', 'CHRISTOLOGIA')

# Fix PREFATORY NOTE<br/>PREFACE being an h2
html = html.replace('<h2 class="contents-treatise-title">PREFATORY NOTE<br/>PREFACE</h2>',
                    '<p class="contents-item" style="text-align: center; margin-top: 1em;">PREFATORY NOTE<br/>PREFACE</p>')

# Fix Chapter 8 being numbered 9.
html = html.replace('<p class="contents-item"><b>9. — </b> Representations of the Glory',
                    '<p class="contents-item"><b>8. — </b> Representations of the Glory')

# Fix PREPATORY NOTE BY THE EDITOR<br/>The Epistle Dedicatory<br/>The Lesser Catechism
html = html.replace('<p class="contents-item">PREPATORY NOTE BY THE EDITOR<br/>The Epistle Dedicatory<br/>The Lesser Catechism</p>',
                    '<p class="contents-item" style="text-align: center; margin-top: 1em;">PREFATORY NOTE BY THE EDITOR<br/>THE EPISTLE DEDICATORY<br/>THE LESSER CATECHISM</p>')

# Fix PREFATORY NOTE BY THE EDITOR<br/>PREFACE TO THE READER
html = html.replace('<h2 class="contents-treatise-title">PREFATORY NOTE BY THE EDITOR<br/>PREFACE TO THE READER</h2>',
                    '<p class="contents-item" style="text-align: center; margin-top: 1em;">PREFATORY NOTE BY THE EDITOR<br/>PREFACE TO THE READER</p>')

# Fix ORIGINAL PREFACE
html = html.replace('<h2 class="contents-treatise-title">ORIGINAL PREFACE</h2>',
                    '<p class="contents-item" style="text-align: center; margin-top: 1em;">ORIGINAL PREFACE</p>')

# Now inject this into volumes/v1/convert.py
with open('volumes/v1/convert.py', 'r') as f:
    convert_py = f.read()

var_code = f"\n_V1_CONTENTS_PAGE = '''{html}'''\n"
convert_py = convert_py.replace('\n_V1_TITLE_SMALL_WORDS = {', var_code + '\n_V1_TITLE_SMALL_WORDS = {')

# Add to overrides
convert_py = convert_py.replace("'treatise_title_overrides': {", "'contents_page_overrides': _V1_CONTENTS_PAGE,\n    'treatise_title_overrides': {")

with open('volumes/v1/convert.py', 'w') as f:
    f.write(convert_py)

print("V1 TOC polished and injected!")
