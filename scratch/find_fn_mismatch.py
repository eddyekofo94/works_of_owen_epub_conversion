import zipfile
import re

for vol in (8, 9, 10):
    epub_path = f'volumes/v{vol}/output/volume_{vol}.epub'
    with zipfile.ZipFile(epub_path, 'r') as z:
        endnotes = ""
        for name in z.namelist():
            if 'endnotes.xhtml' in name:
                endnotes = z.read(name).decode('utf-8')
                break
        
        defined_ids = set()
        if endnotes:
            for m in re.finditer(r'<aside\b[^>]+\bid="(?P<id>fn\d+)"[^>]*>', endnotes):
                defined_ids.add(m.group("id"))
                
        noterefs = {}
        for name in sorted(z.namelist()):
            if name.endswith('.xhtml') and 'ch' in name:
                html = z.read(name).decode('utf-8')
                refs = re.findall(r'href="[^"]*#(fn\d+)"', html)
                if refs:
                    noterefs[name] = refs
                    
        all_referenced = set()
        for refs in noterefs.values():
            all_referenced.update(refs)
            
        print(f"=== Volume {vol} ===")
        print(f"Total endnotes defined: {len(defined_ids)}")
        print(f"Total distinct referenced: {len(all_referenced)}")
        
        orphans = sorted(defined_ids - all_referenced)
        if orphans:
            print(f"Orphans (in endnotes but not in body): {orphans}")
            
        missing_asides = sorted(all_referenced - defined_ids)
        if missing_asides:
            print(f"Missing asides (referenced in body but not in endnotes): {missing_asides}")
            for name, refs in noterefs.items():
                intersection = set(refs) & set(missing_asides)
                if intersection:
                    print(f"  Referenced in {name}: {sorted(intersection)}")
