r"""Audita el portal: pestañas, archivos enlazados y coherencia con los laboratorios."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
texto = (BASE / "index.html").read_text(encoding="utf-8")
script = re.search(r"<script>(.*)</script>", texto, re.S).group(1)

paneles = re.findall(r'data-panel="([^"]+)"[^>]*?(?:data-src="([^"]+)")?', texto)
pestanas = re.findall(r'class="pestana[^"]*" data-panel="([^"]+)"', texto)
fuentes = re.findall(r'data-src="([^"]+)"', texto)
enlaces = re.findall(r'href="(lab0[^"]+)"', texto)

problemas = []
print(f"pestañas: {pestanas}")
print(f"laboratorios incrustados: {fuentes}")

for src in fuentes:
    if not (BASE / src).exists():
        problemas.append(f"el panel apunta a un archivo que no existe: {src}")
    else:
        print(f"  ok    {src} existe ({round((BASE / src).stat().st_size / 1024, 1)} KB)")

for enlace in set(enlaces):
    if not (BASE / enlace).exists():
        problemas.append(f"enlace roto en la guía: {enlace}")

# cada pestaña debe tener su panel y viceversa
for p in pestanas:
    if f'data-panel="{p}"' not in texto.replace(f'data-panel="{p}" role="tab"', f'data-panel="{p}" role="tab"'):
        problemas.append(f"la pestaña {p} no tiene panel")
for src in fuentes:
    nombre = src.replace(".html", "")
    if not any(p in nombre or nombre.split("-")[0] == p for p in pestanas):
        problemas.append(f"el panel {src} no tiene pestaña")

# el portal debe mandar pausar/seguir y los laboratorios deben escucharlo
for palabra in ["postMessage", "'pausar'", "'seguir'", "requestFullscreen", "hashchange"]:
    if palabra not in script:
        problemas.append(f"falta {palabra} en el portal")
for lab in ["lab02-resorte-rlc.html", "lab03-tanque-newton-rc.html"]:
    cuerpo = (BASE / lab).read_text(encoding="utf-8")
    if "addEventListener('message'" not in cuerpo:
        problemas.append(f"{lab} no escucha los mensajes del portal")
    else:
        print(f"  ok    {lab} responde a pausar/seguir")
    if "window.self === window.top" not in cuerpo:
        problemas.append(f"{lab} no detecta que está incrustado")

print()
if problemas:
    for p in problemas:
        print("  FALLA " + p)
    raise SystemExit(1)
print("RESULTADO: portal coherente, todos los archivos y mensajes en orden")
