"""Conservative, text-faithful scholastic anchor annotation."""

import html as html_lib
import re

_PARENT_LABELS = ("Obj", "Objection", "Question", "Inquiry", "Use", "Usus", "Application", "Observation", "Obs")
_CHILD_LABELS = ("Ans", "Answer", "Sol", "Solution", "Response", "Reply")
_ABBREVIATIONS = {"obj", "ans", "sol", "obs"}


def _label_pattern(extra_labels=()):
    labels = sorted(set(_PARENT_LABELS + _CHILD_LABELS + tuple(extra_labels)), key=len, reverse=True)
    return re.compile(
        rf"(?P<word>{'|'.join(re.escape(x) for x in labels)})(?P<space_dot>\s*\.?)\s*"
        rf"(?P<number>\d+)?(?P<number_dot>\s*\.?)",
        re.I,
    )


def normalized_visible_text(fragment: str) -> str:
    """Return visible text normalized only for structural whitespace/entities."""
    text = html_lib.unescape(re.sub(r"<[^>]+>", "", fragment))
    return re.sub(r"\s+", " ", text).strip()


def _family(word: str, extra_parent=(), extra_child=()):
    low = word.lower()
    if low in {w.lower() for w in _PARENT_LABELS + tuple(extra_parent)}:
        return "parent"
    if low in {w.lower() for w in _CHILD_LABELS + tuple(extra_child)}:
        return "child"
    return None


def _safe_label(match, *, active_parent, extra_parent=(), extra_child=()):
    word = match.group("word")
    family = _family(word, extra_parent, extra_child)
    number = match.group("number")
    low = word.lower()
    has_period = "." in match.group("space_dot")
    if family is None or (low in _ABBREVIATIONS and not has_period):
        return None
    if low in {"use", "answer", "solution", "response", "reply", "observation", "question", "inquiry"} and not number and not has_period:
        return None
    if low == "use" and not number:
        return None
    if family == "child" and not number and not active_parent:
        return None
    label = word + ("." if has_period else "")
    if number:
        label += f" {number}" + ("." if "." in match.group("number_dot") else "")
    return family, label


def _add_classes(open_tag, *classes):
    attrs = open_tag[2:-1]
    match = re.search(r'\bclass="([^"]*)"', attrs, re.I)
    existing = match.group(1).split() if match else []
    existing = [c for c in existing if c not in {"list-item", "roman-list-item"} and not c.startswith("list-level-")]
    for cls in classes:
        if cls not in existing:
            existing.append(cls)
    if match:
        attrs = attrs[:match.start()] + f'class="{" ".join(existing)}"' + attrs[match.end():]
    else:
        attrs += f' class="{" ".join(existing)}"'
    return f"<p{attrs}>"


def apply_scholastic_anchor_protocol(html: str, config: dict | None = None) -> str:
    """Annotate strict labels without synthesizing label words or numbers."""
    if not html:
        return html
    config = config or {}
    extra_parent = tuple(config.get("scholastic_parent_labels", ()))
    extra_child = tuple(config.get("scholastic_child_labels", ()))
    pattern = _label_pattern(extra_parent + extra_child)
    block_re = re.compile(r"(<blockquote\b.*?</blockquote>|<aside\b.*?</aside>|<p\b[^>]*>.*?</p>)", re.I | re.S)
    output, last, active_parent = [], 0, False
    for found in block_re.finditer(html):
        output.append(html[last:found.start()])
        block, last = found.group(0), found.end()
        if not block.lower().startswith("<p"):
            output.append(block)
            continue
        open_end = block.find(">") + 1
        open_tag, inner = block[:open_end], block[open_end:-4]
        strong = re.match(r"\s*<(?:strong|b)(?:\s[^>]*)?>(?P<label>.*?)</(?:strong|b)>\s*", inner, re.I | re.S)
        source = normalized_visible_text(strong.group("label") if strong else inner)
        candidate = pattern.match(source)
        safe = _safe_label(candidate, active_parent=active_parent, extra_parent=extra_parent, extra_child=extra_child) if candidate else None
        if not safe:
            output.append(block)
            active_parent = False
            continue
        family, clean_label = safe
        if strong:
            consumed = strong.end()
        else:
            number = candidate.group("number")
            prefix = re.compile(rf"^\s*{re.escape(candidate.group('word'))}\s*\.?(?:\s*{number}\s*\.?)?\s*" if number else rf"^\s*{re.escape(candidate.group('word'))}\s*\.?\s*", re.I)
            raw = prefix.match(inner)
            if not raw:
                output.append(block)
                continue
            consumed = raw.end()
        open_tag = _add_classes(open_tag, "scholastic-anchor", f"scholastic-{family}", f"scholastic-anchor-{family}")
        output.append(f'{open_tag}<strong class="scholastic-label">{clean_label}</strong> {inner[consumed:].lstrip()}</p>')
        active_parent = active_parent or family == "parent"
    output.append(html[last:])
    return "".join(output)
