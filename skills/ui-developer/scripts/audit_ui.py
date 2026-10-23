#!/usr/bin/env python3
"""Audit UI files written by the ui-developer skill.

Usage:  python3 -I audit_ui.py [--css BUILT.css] FILE [FILE ...]

Checks (FAIL exits 1):
  FAIL    <style> blocks, style attributes that set anything but a --live-* custom property
  FAIL    hex / rgb() / hsl() / oklch() literals, --primitive-* tokens, named colors in classes
  FAIL    arbitrary values in utilities (p-[13px], bg-[#fff]); (--token) pass-through is allowed
  FAIL    with --css: a utility class that is absent from the built CSS (Tailwind ignores
          unknown classes silently, so absence means the class does nothing)
  REPORT  runtime style custom properties (list them in the reply), PLACEHOLDER-DATA markers
"""
import re
import sys
from pathlib import Path

FAMILIES = (
    "bg|text|border|ring|outline|fill|stroke|shadow|rounded|size|min-h|max-h|h|min-w|max-w|w|"
    "p|px|py|pt|pb|pl|pr|ps|pe|m|mx|my|mt|mb|ml|mr|ms|me|gap|gap-x|gap-y|space-x|space-y|z|ease|"
    "duration|delay|opacity|leading|tracking|font|grid-cols|grid-rows|col-span|row-span|order|"
    "inset|top|bottom|left|right|start|end|divide|translate-x|translate-y|scale|rotate|origin|"
    "transition|animate|aspect|basis|line-clamp|decoration|underline-offset|accent|caret|"
    "from|via|to|backdrop|blur|columns"
)
NAMED_COLOR = r"(?:white|black|red|blue|green|yellow|orange|purple|pink|gray|grey|slate|zinc|neutral|stone|amber|lime|emerald|teal|cyan|sky|indigo|violet|fuchsia|rose|transparent|current)"
STRING_RE = re.compile(r"""(?:"([^"\n]*)"|'([^'\n]*)'|`([^`]*)`)""")
UTILITY_RE = re.compile(rf"^(?:!)?-?(?:{FAMILIES})(?:-[^\s]+)?$")
# Variants with an attribute selector in brackets are allowed: data-[open]:, aria-[x=y]:, group-data-[...]:
ALLOWED_VARIANT_BRACKET = re.compile(r"^(?:group-|peer-)?(?:data|aria)-\[[a-z0-9_=\-]+\]$")


def split_variants(token):
    """Split 'hover:data-[open]:bg-brand' into (variants, utility), ignoring ':' inside brackets."""
    parts, depth, cur = [], 0, ""
    for ch in token:
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth -= 1
        if ch == ":" and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts, cur


def css_escape(token):
    return re.sub(r"([^a-zA-Z0-9_-])", r"\\\1", token)


def class_tokens(text):
    seen = {}
    for m in STRING_RE.finditer(text):
        s = next(g for g in m.groups() if g is not None)
        s = re.sub(r"\$\{[^}]*\}", " ", s)  # drop template expressions
        toks = s.split()
        cands = [t for t in toks if split_variants(t)[1] and UTILITY_RE.match(split_variants(t)[1])]
        # Only treat a string as a class list if most of its words look like utilities.
        if cands and len(cands) * 2 >= len(toks):
            for t in cands:
                seen.setdefault(t, m.start())
    return seen


def main(argv):
    css_path, files = None, []
    it = iter(argv)
    for a in it:
        if a == "--css":
            css_path = next(it, None)
        else:
            files.append(a)
    if not files:
        print(__doc__)
        return 2
    css = Path(css_path).read_text(errors="replace") if css_path else None
    fails, reports = [], []

    for f in files:
        p = Path(f)
        if not p.is_file():
            fails.append(f"{f}: file not found")
            continue
        text = p.read_text(errors="replace")
        lines = text.splitlines()

        def at(pos):
            return text.count("\n", 0, pos) + 1

        if p.suffix in {".css", ".scss", ".sass", ".less"}:
            reports.append(f"{f}: stylesheet in the changed set; only unedited design-system copies are allowed")
        for m in re.finditer(r"<style\b", text):
            fails.append(f"{f}:{at(m.start())}: <style> block")
        for m in re.finditer(r"""style\s*=\s*(?:\{\{(.*?)\}\}|"([^"]*)"|'([^']*)')""", text, re.S):
            body = next((g for g in m.groups() if g is not None), "")
            keys = re.findall(r"""['"]?([-\w]+)['"]?\s*:""", body)
            if keys and all(k.startswith("--live-") for k in keys):
                reports.append(f"{f}:{at(m.start())}: runtime style {', '.join(keys)}")
            else:
                fails.append(f"{f}:{at(m.start())}: inline style (only --live-* custom properties are allowed)")
        for i, line in enumerate(lines, 1):
            if re.search(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch|color)\(|--primitive-", line):
                if "PLACEHOLDER" not in line:
                    fails.append(f"{f}:{i}: raw color value or primitive token: {line.strip()[:80]}")
            if "PLACEHOLDER-DATA" in line:
                reports.append(f"{f}:{i}: {line.strip()[:100]}")

        for tok, pos in class_tokens(text).items():
            variants, util = split_variants(tok)
            for v in variants:
                if "[" in v and not ALLOWED_VARIANT_BRACKET.match(v):
                    fails.append(f"{f}:{at(pos)}: arbitrary variant '{v}' in '{tok}'")
            if re.search(r"\[[^\]]*\]", util):
                fails.append(f"{f}:{at(pos)}: arbitrary value in '{tok}'")
            elif re.search(rf"-{NAMED_COLOR}(?:-\d{{2,3}})?(?:/\d+)?$", util) and re.match(r"^(?:bg|text|border|ring|outline|fill|stroke|from|via|to|accent|caret|decoration)-", util):
                fails.append(f"{f}:{at(pos)}: stock color '{tok}'")
            elif css is not None and "." + css_escape(tok) not in css:
                fails.append(f"{f}:{at(pos)}: '{tok}' is not in the built CSS (unknown class, silently ignored)")

    for r in reports:
        print("REPORT", r)
    for x in fails:
        print("FAIL  ", x)
    print(f"\n{len(fails)} failure(s), {len(reports)} item(s) to report."
          + ("" if css is not None else " Class existence NOT checked (no --css given)."))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
