"""Build the GitHub Pages site in docs/ from ai_agent_actions_profile.json.

Run after tools/build_profile.py:  python3 tools/build_site.py
Writes docs/index.html (human-readable, one anchor per concept), docs/profile.json
(the profile document) and docs/.nojekyll. Concept anchors are the IRI path
with "/" replaced by "-", e.g. verbs/perceived -> #verbs-perceived.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://w3id.org/xapi-ai/"
p = json.loads((ROOT / "ai_agent_actions_profile.json").read_text())


def anchor(iri: str) -> str:
    return iri.removeprefix(BASE).replace("/", "-") if iri.startswith(BASE) else ""


def e(s) -> str:
    return html.escape(str(s), quote=True)


def matches(c) -> str:
    out = []
    for k in ("exactMatch", "broadMatch", "narrowMatch", "relatedMatch"):
        for iri in c.get(k, []):
            label = iri.rsplit("/", 1)[-1]
            out.append(f'<a href="{e(iri)}">{e(label)}</a> <span class="rel">({k})</span>')
    return "; ".join(out) or "—"


SECTIONS = [("Verb", "Verbs"), ("ActivityType", "Activity types"),
            ("ContextExtension", "Context extensions"), ("ResultExtension", "Result extensions")]
version = p["versions"][0]["id"].rsplit("/", 1)[-1]
rows = []
for kind, title in SECTIONS:
    cs = [c for c in p["concepts"] if c["type"] == kind]
    rows.append(f'<section aria-labelledby="h-{kind}"><h2 id="h-{kind}">{title} ({len(cs)})</h2>')
    rows.append('<table><thead><tr><th scope="col">Label</th><th scope="col">IRI</th>'
                '<th scope="col">Definition</th><th scope="col">Since</th><th scope="col">I2IDL Glossary</th></tr></thead><tbody>')
    for c in cs:
        since = c["inScheme"].rsplit("/", 1)[-1]
        rows.append(f'<tr id="{e(anchor(c["id"]))}"><th scope="row">{e(c["prefLabel"]["en"])}</th>'
                    f'<td><code>{e(c["id"])}</code></td><td>{e(c["definition"]["en"])}</td>'
                    f'<td>{e(since)}</td><td>{matches(c)}</td></tr>')
    rows.append("</tbody></table></section>")
tpl = [f'<li id="{e(anchor(t["id"]))}"><strong>{e(t["prefLabel"]["en"])}</strong>: {e(t["definition"]["en"])} '
       f'<code>{e(t["id"])}</code></li>' for t in p["templates"]]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["prefLabel"]["en"])} {e(version)}</title>
<link rel="alternate" type="application/ld+json" href="profile.json">
<style>
:root {{ --bg:#fff; --fg:#1a1a1a; --muted:#555; --line:#ccc; --link:#0b5394; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#111; --fg:#eee; --muted:#bbb; --line:#444; --link:#8ab4f8; }} }}
body {{ font: 16px/1.55 system-ui, sans-serif; background:var(--bg); color:var(--fg); margin:0 auto; max-width:72rem; padding:1rem; }}
a {{ color:var(--link); }} code {{ font-size:.85em; word-break:break-all; }}
table {{ border-collapse:collapse; width:100%; margin:1rem 0 2rem; }}
th, td {{ border:1px solid var(--line); padding:.4rem .5rem; text-align:left; vertical-align:top; }}
tr:target {{ outline:3px solid var(--link); }} .rel, .muted {{ color:var(--muted); }}
.skip {{ position:absolute; left:-999px; }} .skip:focus {{ left:1rem; top:1rem; background:var(--bg); padding:.5rem; }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
<h1>{e(p["prefLabel"]["en"])}</h1>
<p>Version <strong>{e(version)}</strong>. Profile IRI <code>{e(p["id"])}</code>.
<a href="profile.json">Profile document (JSON-LD)</a> ·
<a href="https://github.com/seanrugg/xapi-ai">Source</a> ·
<a href="https://github.com/seanrugg/xapi-ai/blob/main/ROBOTICS_MODULE.md">Robotics module and mapping</a> ·
<a href="https://github.com/seanrugg/xapi-ai/blob/main/GAPS.md">Glossary gaps</a></p>
<p>{e(p["definition"]["en"])}</p>
</header>
<main id="main">
{"".join(rows)}
<section aria-labelledby="h-templates"><h2 id="h-templates">Statement templates ({len(p["templates"])})</h2><ul>{"".join(tpl)}</ul></section>
</main>
<footer class="muted"><p>Generated from <code>ai_agent_actions_profile.json</code> by <code>tools/build_site.py</code>.</p></footer>
</body>
</html>
"""
docs = ROOT / "docs"
docs.mkdir(exist_ok=True)
(docs / "index.html").write_text(page)
shutil.copy(ROOT / "ai_agent_actions_profile.json", docs / "profile.json")
(docs / ".nojekyll").write_text("")
print(f"wrote docs/index.html, docs/profile.json ({len(p['concepts'])} concepts)")
