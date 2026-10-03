#!/usr/bin/env python3
"""
Wraps CMS fragment files into full HTML pages for Vercel preview deployment.
Output structure mirrors the live URL paths:
  index.html                          ← /sl/glosar/
  vrste-kritine/index.html            ← /sl/glosar/vrste-kritine/
  profili-stresnikov/index.html       ← ...
  etc.
"""

import os, re

REPO = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    ("glossary-00-parent.html",           ".",                       "Glosar strešnih pojmov GERARD"),
    ("glossary-01-vrste-kritine.html",    "vrste-kritine",           "Vrste strešnih kritin — Glosar GERARD"),
    ("glossary-02-profili-stresnikov.html","profili-stresnikov",     "Profili in oblike strešnikov — Glosar GERARD"),
    ("glossary-03-material-in-zlitine.html","material-in-zlitine",   "Material in jeklene zlitine — Glosar GERARD"),
    ("glossary-04-posip-in-barve.html",   "posip-in-barve",          "Kamniti posip in barvne možnosti — Glosar GERARD"),
    ("glossary-05-konstrukcija-strehe.html","konstrukcija-strehe",   "Konstrukcija in elementi strehe — Glosar GERARD"),
    ("glossary-06-montaza-in-instalacija.html","montaza-in-instalacija","Montaža strešnikov — Glosar GERARD"),
    ("glossary-07-vremenski-vplivi.html", "vremenski-vplivi",        "Odpornost in vremenski vplivi — Glosar GERARD"),
    ("glossary-08-menjava-kritine.html",  "menjava-kritine",         "Menjava in sanacija kritine — Glosar GERARD"),
    ("glossary-09-stresni-dodatki.html",  "stresni-dodatki",         "Strešni preboji in dodatki — Glosar GERARD"),
    ("glossary-10-trajnostnost.html",     "trajnostnost",            "Trajnostnost in ekologija — Glosar GERARD"),
    ("glossary-11-garancija-standardi.html","garancija-standardi",   "Garancija in certifikati — Glosar GERARD"),
    ("glossary-12-krovska-terminologija.html","krovska-terminologija","Krovska dela in terminologija — Glosar GERARD"),
]

WRAPPER = """\
<!doctype html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="robots" content="noindex">
<style>
  body {{ margin: 0; padding: 24px 0; background: #fff; }}
</style>
</head>
<body>
{fragment}
</body>
</html>"""

built = 0
for src_name, out_dir, title in PAGES:
    src = os.path.join(REPO, src_name)
    with open(src, encoding="utf-8") as f:
        fragment = f.read()

    html = WRAPPER.format(title=title, fragment=fragment)

    if out_dir == ".":
        out_path = os.path.join(REPO, "index.html")
    else:
        dir_path = os.path.join(REPO, out_dir)
        os.makedirs(dir_path, exist_ok=True)
        out_path = os.path.join(dir_path, "index.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    built += 1
    print(f"  ✓  {out_path.replace(REPO, '')}")

print(f"\nBuilt {built} pages.")
