Created At: 2026-05-29T17:46:55Z
Completed At: 2026-05-29T17:46:55Z
File Path: `file:///Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/render.py`
Total Lines: 5051
Total Bytes: 226473
Showing lines 2620 to 2660
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
2620:         return 'list-level-1', 'roman_decimal'
2621: 
2622:     return 'list-level-1', previous_marker_family or 'other'
2623: 
2624: 
2625: def _add_owen_list_level_classes(html: str) -> str:
2626:     """Add modest reader-facing hierarchy classes to remaining block lists."""
2627:     item_re = re.compile(
2628:         r'<p class="(?P<class>list-item|roman-list-item)">(?P<inner>.*?)</p>',
2629:         re.S,
2630:     )
2631:     previous_family = None
2632: 
2633:     def repl(match: re.Match) -> str:
2634:         nonlocal previous_family
2635:         cls = match.group('class')
2636:         inner = match.group('inner')
2637:         marker_match = re.match(r'\s*(<b>[^<]{1,40}</b>)', inner, re.S)
2638: 
2639:         if cls == 'roman-list-item':
2640:             previous_family = 'roman'
2641:             return f'<p class="{cls} list-level-1">{inner}</p>'
2642: 
2643:         level_class, family = _owen_marker_level(
2644:             marker_match.group(1) if marker_match else '',
2645:             previous_family,
2646:         )
2647:         previous_family = family
2648:         return f'<p class="{cls} {level_class}">{inner}</p>'
2649: 
2650:     return item_re.sub(repl, html)
2651: 
2652: 
2653: # ---------------------------------------------------------------------------
2654: # Issue #16: Em-dash introduced flat list
2655: # ---------------------------------------------------------------------------
2656: 
2657: #: Per-item word cap: if ANY item in a list run exceeds this many content words
2658: #: the run is left as a block list regardless of other signals.
2659: # Raised from 8→12 (Bug #6): Owen's numbered parallel items like
2660: # "1. That God hath done it. 2. That he hath promised he will yet do it.
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
