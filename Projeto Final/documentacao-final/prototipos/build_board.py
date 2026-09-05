#!/usr/bin/env python3
# Junta as 10 telas (mobile + desktop) num único HTML autocontido,
# escopando cada CSS sob um wrapper para não colidir.
import re, os
BASE = os.path.dirname(os.path.abspath(__file__))

def strip_comments(css): return re.sub(r'/\*.*?\*/', '', css, flags=re.S)

def parse_blocks(s):
    res, i, start = [], 0, 0
    while i < len(s):
        if s[i] == '{':
            selector = s[start:i].strip()
            depth, j = 1, i + 1
            while j < len(s) and depth > 0:
                if s[j] == '{': depth += 1
                elif s[j] == '}': depth -= 1
                j += 1
            res.append((selector, s[i+1:j-1]))
            i = start = j
        else:
            i += 1
    return res

def prefix_sel(sellist, scope):
    out = []
    for p in [x.strip() for x in sellist.split(',') if x.strip()]:
        if p == ':root': out.append(scope)
        elif p.startswith(':root'): out.append(scope + p[5:])
        elif p in ('html', 'body'): out.append(scope)
        elif p == '*': out.append(scope + ' *')
        else: out.append(scope + ' ' + p)
    return ', '.join(out)

def scope_css(css, scope):
    css = strip_comments(css)
    out = []
    for sel, body in parse_blocks(css):
        if sel.startswith('@media'):
            inner = ''.join(f"{prefix_sel(s, scope)}{{{b}}}" for s, b in parse_blocks(body))
            out.append(f"{sel}{{{inner}}}")
        elif sel.startswith('@'):
            out.append(f"{sel}{{{body}}}")
        else:
            out.append(f"{prefix_sel(sel, scope)}{{{body}}}")
    return '\n'.join(out)

def body_inner(path):
    html = open(path, encoding='utf-8').read()
    return re.search(r'<body>(.*)</body>', html, re.S).group(1).strip()

mob_css = scope_css(open(f"{BASE}/mobile/eduhub-mobile.css", encoding='utf-8').read(), '#board-mobile')
desk_css = scope_css(open(f"{BASE}/desktop/eduhub-desktop.css", encoding='utf-8').read(), '#board-desktop')

mobile = [("m-01-login","Login"),("m-02-home","Home"),("m-03-notas","Notas"),
          ("m-04-frequencia","Frequência"),("m-05-periodos","Períodos")]
desktop = [("d-01-login","Login"),("d-02-home","Início"),("d-03-notas","Lançamento de Notas"),
           ("d-04-frequencia","Frequência"),("d-05-periodos","Períodos Letivos")]

mob_html = "\n".join(body_inner(f"{BASE}/mobile/{f}.html") for f,_ in mobile)
desk_html = "\n".join(
    f'<div class="dwrap"><div class="dlabel">{lbl}</div>{body_inner(f"{BASE}/desktop/{f}.html")}</div>'
    for f, lbl in desktop)

page = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EduHub — Todas as telas (CU-03)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;background:#e9ece9;font-family:"Inter","Segoe UI",system-ui,sans-serif}}
.board-title{{font-weight:800;font-size:24px;color:#12362C;padding:30px 30px 2px}}
.board-sub{{font-weight:700;font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#5c6b63;padding:22px 30px 10px}}
#board-mobile{{display:flex;flex-wrap:wrap;align-items:flex-start;background:#e9ece9}}
#board-desktop .dwrap{{padding:22px 30px 6px}}
#board-desktop .dlabel{{font-weight:600;font-size:13px;color:#5c6b63;margin-bottom:10px}}
{mob_css}
{desk_css}
#board-desktop .page{{min-height:0 !important}}
#board-desktop .auth{{min-height:600px !important}}
</style>
</head>
<body>
<div class="board-title">EduHub — Protótipos do fluxo CU-03</div>
<div class="board-sub">Aplicativo (mobile)</div>
<div id="board-mobile">
{mob_html}
</div>
<div class="board-sub">Web (desktop)</div>
<div id="board-desktop">
{desk_html}
</div>
</body>
</html>
"""
out = f"{BASE}/figma/eduhub-todas-telas.html"
open(out, "w", encoding="utf-8").write(page)
print("gerado:", os.path.basename(out), f"{len(page)//1024}KB")
