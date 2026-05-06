import re
import os

def safe_fix():
    with open('books/Owen/volumes/v1/intermediate/volume_1.thml.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Re-apply TOC and Greek fix
    old_ch001 = """    <div1 title="CONTENTS OF VOLUME 1. — : OR, A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST. — CHAPTER 1." id="ch001">
      <h2>CONTENTS OF VOLUME 1. — : OR, A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST. — CHAPTER 1.</h2>
      <p class="Body">
        <span style="font-variant:small-caps">REFATORY </span>
        <span style="font-variant:small-caps">OTE </span>
        <span style="font-variant:small-caps">REFACE </span>
      </p>
      <p class="Body">Peter’s Confession; Matthew 16:16 — Conceits of the Papists thereon — The Substance and Excellency of that Confession. </p>
    </div1>"""

    new_ch001 = """    <div1 title="CONTENTS OF VOLUME 1" id="ch001">
      <h2>CONTENTS OF VOLUME 1</h2>
      <p class="Body">
        <span lang="EL" class="Greek">ΧΡΙΣΤΟΛΟΓΙΑ</span>: <span style="font-variant:small-caps">OR, A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST</span>
      </p>
      <p class="Body">Prefatory Note</p>
      <p class="Body">Preface</p>
      <p class="Body"><b>1.</b> — Peter’s Confession; Matthew 16:16 — Conceits of the Papists thereon — The Substance and Excellency of that Confession.</p>
      <p class="Body"><b>2.</b> — Opposition made unto the Church as built upon the Person of Christ.</p>
      <p class="Body"><b>3.</b> — The Person of Christ the most ineffable effect of divine wisdom and goodness — thence the next cause of all true religion — in what sense it is so.</p>
      <p class="Body"><b>4.</b> — The Person of Christ the foundation of all the counsels of God.</p>
      <p class="Body"><b>5.</b> — The Person of Christ the great representative of God and his will.</p>
      <p class="Body"><b>6.</b> — The Person of Christ the great repository of sacred truth — its relation thereunto.</p>
      <p class="Body"><b>7.</b> — Power and efficacy communicated unto the office of Christ, for the salvation of the church, from his person.</p>
      <p class="Body"><b>8.</b> — The Faith of the Church under the Old Testament in and concerning the Person of Christ.</p>
      <p class="Body"><b>9.</b> — Honor due to the Person of Christ — the nature and causes of it.</p>
      <p class="Body"><b>10.</b> — The Principle of the Assignation of Divine Honor unto the Person of Christ, in both the branches of it; with his Faith in Him.</p>
      <p class="Body"><b>11.</b> — Obedience unto Christ — the nature and causes of it.</p>
      <p class="Body"><b>12.</b> — The Especial Principle of Obedience unto the Person of Christ; which is Love — its Truth and Reality vindicated.</p>
      <p class="Body"><b>13.</b> — The Nature, Operations, and Causes of Divine Love, as it respects the Person of Christ.</p>
      <p class="Body"><b>14.</b> — Motives unto the Love of Christ.</p>
      <p class="Body"><b>15.</b> — Conformity unto Christ, and following his Example.</p>
      <p class="Body"><b>16.</b> — An humble inquiry into, and prospect of, the infinite wisdom of God, in the constitution of the person of Christ, and the way of salvation thereby.</p>
      <p class="Body"><b>17.</b> — Other evidences of divine wisdom in the contrivance of the work of redemption in and by the person of Christ, in effects evidencing a condecency thereunto.</p>
      <p class="Body"><b>18.</b> — The nature of the person of Christ, and the hypostatical union of his natures declared.</p>
      <p class="Body"><b>19.</b> — The exaltation of Christ, with his present state and condition in glory during the continuance of his mediatory office.</p>
      <p class="Body"><b>20.</b> — The exercise of the mediatory office of Christ in heaven.</p>
    </div1>"""

    # Replace ch001 carefully
    # Find exact range to avoid regex greed
    start_tag = '<div1 title="CONTENTS OF VOLUME 1. — : OR, A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST. — CHAPTER 1." id="ch001">'
    end_tag = '</div1>'
    idx_start = content.find(start_tag)
    if idx_start != -1:
        idx_end = content.find(end_tag, idx_start)
        if idx_end != -1:
            idx_end += len(end_tag)
            content = content[:idx_start] + new_ch001 + content[idx_end:]
            print("Fixed ch001")

    # Helper to remove a div1 by ID and return its inner content
    def extract_and_remove(cid, text):
        pattern = fr'(    <div1[^>]*id="{cid}"[^>]*>.*?<\/div1>)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            # Extract inner content (after <h2>...</h2>)
            inner_match = re.search(r'<h2>.*?<\/h2>(.*?)<\/div1>', match.group(0), re.DOTALL)
            inner_content = inner_match.group(1).strip() if inner_match else ""
            title_match = re.search(r'title="([^"]*)"', match.group(0))
            title = title_match.group(1) if title_match else ""
            
            # Remove from text
            text = text[:match.start()] + text[match.end():]
            return text, title, inner_content
        return text, None, None

    # Fix ch019 (Ghost IV for Chapter 9)
    # We'll just delete it as it's redundant.
    content, t, c = extract_and_remove('ch019', content)
    if t: print(f"Removed Ghost {t} (ch019)")

    # Fix ch033 (Ghost IV for Chapter 18)
    content, t, c = extract_and_remove('ch033', content)
    if t: print(f"Removed Ghost {t} (ch033)")

    # Fix Preface (ch047 + ch048-ch051)
    reasons = ""
    for cid in ['ch048', 'ch049', 'ch050', 'ch051']:
        content, title, inner = extract_and_remove(cid, content)
        if title:
            reasons += f'\n      <p class="Body">\n        <b>{title} </b>\n        {inner}\n      </p>'
    
    if reasons:
        # Append to ch047
        idx = content.find('id="ch047"')
        if idx != -1:
            idx_end = content.find('</div1>', idx)
            content = content[:idx_end] + reasons + "\n    " + content[idx_end:]
            print("Merged Preface reasons")

    # Fix Chapter 2 Summaries (ch080 + ch081-ch084)
    summaries = ""
    for cid in ['ch081', 'ch082', 'ch083', 'ch084']:
        content, title, inner = extract_and_remove(cid, content)
        if title:
            summaries += f'\n      <p class="Body">\n        <b>{title} </b>\n        {inner}\n      </p>'
            
    if summaries:
        idx = content.find('id="ch080"')
        if idx != -1:
            idx_end = content.find('</div1>', idx)
            content = content[:idx_end] + summaries + "\n    " + content[idx_end:]
            print("Merged Chapter 2 summaries")

    # Case 5: Chapter 19 Summaries (ch038 + ch039-ch040)
    ch19_sums = ""
    for cid in ['ch039', 'ch040']:
        content, title, inner = extract_and_remove(cid, content)
        if title:
            ch19_sums += f'\n      <p class="Body">\n        <b>{title} </b>\n        {inner}\n      </p>'
            
    if ch19_sums:
        idx = content.find('id="ch038"')
        if idx != -1:
            idx_end = content.find('</div1>', idx)
            content = content[:idx_end] + ch19_sums + "\n    " + content[idx_end:]
            print("Merged Chapter 19 summaries")

    with open('books/Owen/volumes/v1/intermediate/volume_1.thml.xml', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    safe_fix()
