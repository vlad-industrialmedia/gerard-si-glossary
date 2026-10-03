#!/usr/bin/env python3
"""
Wraps CMS fragment files into full HTML pages for Vercel preview deployment.

Source fragments (glossary-00…12.html) keep production-ready URLs:
  /sl/glosar/              → hub
  /sl/glosar/vrste-kritine/ → cluster 01
  etc.

The Vercel wrapper rewrites only GLOSSARY-internal hrefs so navigation works
on the preview deployment. All /sl/... links that point outside the glossary
(e.g. /sl/zakaj-gerard/) are left as-is — they are dead on Vercel preview,
which is intentional. Devs pull the source fragments from GitHub and deploy
with /sl/glosar/ prefix — no changes needed.

URL structure for Vercel preview:
  index.html                     ← /
  vrste-kritine/index.html       ← /vrste-kritine/
  profili-stresnikov/index.html  ← /profili-stresnikov/
  … (12 clusters)
"""

import os, re

REPO = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    ("glossary-00-parent.html",            ".",                        "Glosar strešnih pojmov GERARD"),
    ("glossary-01-vrste-kritine.html",     "vrste-kritine",            "Vrste strešnih kritin — Glosar GERARD"),
    ("glossary-02-profili-stresnikov.html","profili-stresnikov",       "Profili in oblike strešnikov — Glosar GERARD"),
    ("glossary-03-material-in-zlitine.html","material-in-zlitine",     "Material in jeklene zlitine — Glosar GERARD"),
    ("glossary-04-posip-in-barve.html",    "posip-in-barve",           "Kamniti posip in barvne možnosti — Glosar GERARD"),
    ("glossary-05-konstrukcija-strehe.html","konstrukcija-strehe",     "Konstrukcija in elementi strehe — Glosar GERARD"),
    ("glossary-06-montaza-in-instalacija.html","montaza-in-instalacija","Montaža strešnikov — Glosar GERARD"),
    ("glossary-07-vremenski-vplivi.html",  "vremenski-vplivi",         "Odpornost in vremenski vplivi — Glosar GERARD"),
    ("glossary-08-menjava-kritine.html",   "menjava-kritine",          "Menjava in sanacija kritine — Glosar GERARD"),
    ("glossary-09-stresni-dodatki.html",   "stresni-dodatki",          "Strešni preboji in dodatki — Glosar GERARD"),
    ("glossary-10-trajnostnost.html",      "trajnostnost",             "Trajnostnost in ekologija — Glosar GERARD"),
    ("glossary-11-garancija-standardi.html","garancija-standardi",     "Garancija in certifikati — Glosar GERARD"),
    ("glossary-12-krovska-terminologija.html","krovska-terminologija", "Krovska dela in terminologija — Glosar GERARD"),
]

# All 12 cluster slugs — used to scope the rewrite to glossary links only
CLUSTER_SLUGS = [
    "vrste-kritine", "profili-stresnikov", "material-in-zlitine",
    "posip-in-barve", "konstrukcija-strehe", "montaza-in-instalacija",
    "vremenski-vplivi", "menjava-kritine", "stresni-dodatki",
    "trajnostnost", "garancija-standardi", "krovska-terminologija",
]

def rewrite_for_vercel(html: str) -> str:
    """
    Rewrites glossary-internal hrefs from production paths to Vercel preview paths.

    Production path                 → Vercel preview path
    /sl/glosar/                     → /
    /sl/glosar/vrste-kritine/       → /vrste-kritine/
    /sl/glosar/vrste-kritine/#term  → /vrste-kritine/#term

    Rules:
    - Only rewrites href values that start with /sl/glosar/
    - Preserves anchor fragments (#…) on cluster links
    - Does NOT touch /sl/... paths outside the glossary (e.g. /sl/montaza/)
    """
    # 1. Hub breadcrumb / nav link: href="/sl/glosar/"  →  href="/"
    html = re.sub(r'href="/sl/glosar/"', 'href="/"', html)

    # 2. Cluster links with optional anchor: href="/sl/glosar/SLUG/"  →  href="/SLUG/"
    #    Also matches href="/sl/glosar/SLUG/#anchor"
    slugs_pattern = "|".join(re.escape(s) for s in CLUSTER_SLUGS)
    html = re.sub(
        r'href="/sl/glosar/(' + slugs_pattern + r')/(#[^"]*)?\"',
        lambda m: f'href="/{m.group(1)}/{m.group(2) or ""}"',
        html,
    )

    return html

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

    # Rewrite glossary-internal links for Vercel preview
    fragment_vercel = rewrite_for_vercel(fragment)

    html = WRAPPER.format(title=title, fragment=fragment_vercel)

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
print("Source fragments (glossary-*.html) unchanged — use as-is for /sl/glosar/ on gerardroofs.si")
