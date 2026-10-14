r"""Audita la interfaz de los laboratorios: identificadores, ayudas y estructura."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
total_fallos = 0

for ruta in sorted(BASE.glob("lab0*.html")):
    texto = ruta.read_text(encoding="utf-8")
    script = re.search(r"<script>(.*)</script>", texto, re.S).group(1)
    html = texto[:texto.index("<script>")]

    ids_html = set(re.findall(r'id="([^"]+)"', texto))
    ids_js = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", script))
    faltan = sorted(i for i in ids_js if i not in ids_html)

    # variables de estado declaradas antes de usarse en la interfaz
    declaradas = set(re.findall(r"\b(?:let|const|var)\s+([A-Za-z_$][\w$]*)", script))
    usadas_interfaz = set(re.findall(r"(?<!['\"])\b(pausado|panelLateral|btnPausa|btnPlegar)\b", script))
    sin_declarar = sorted(u for u in usadas_interfaz if u not in declaradas)

    ayudas = len(re.findall(r'class="ayuda"', texto))
    chips = len(re.findall(r'class="chip', texto))
    medidores = len(re.findall(r'class="fila-medidor"', texto))
    tiene_guia = 'id="bienvenida"' in texto
    tiene_avisos = 'id="avisos"' in texto
    tiene_plegar = 'id="btnPlegar"' in texto
    css_nuevo = '--radio:13px' in texto

    # cobertura del CSS: toda clase usada en el HTML debe estar definida
    estilo = re.search(r"<style>(.*?)</style>", texto, re.S).group(1)
    clases_css = set(re.findall(r"\.([a-zA-Z][\w-]*)", estilo))
    clases_html = set()
    for atributo in re.findall(r'class="([^"]+)"', html):
        clases_html.update(atributo.split())
    sin_estilo = sorted(c for c in clases_html if c not in clases_css)

    problemas = []
    if faltan:
        problemas.append(f"getElementById sin elemento: {faltan}")
    if sin_declarar:
        problemas.append(f"variables usadas sin declarar: {sin_declarar}")
    if sin_estilo:
        problemas.append(f"clases sin estilo definido: {sin_estilo}")
    for nombre, valor in [("guía", tiene_guia), ("avisos", tiene_avisos), ("panel plegable", tiene_plegar),
                          ("hoja de estilos nueva", css_nuevo)]:
        if not valor:
            problemas.append(f"falta {nombre}")

    print(f"=== {ruta.name} ===")
    print(f"  ids en el HTML: {len(ids_html)} · referenciados en JS: {len(ids_js)} · "
          f"ayudas: {ayudas} · chips: {chips} · medidores: {medidores} · "
          f"clases: {len(clases_html)} usadas / {len(clases_css)} definidas")
    if problemas:
        total_fallos += 1
        for p in problemas:
            print("  FALLA " + p)
    else:
        print("  ok    interfaz coherente: todos los identificadores existen y los elementos están")

print("\nRESULTADO:", "interfaz verificada en todos los laboratorios" if total_fallos == 0
      else f"{total_fallos} laboratorio(s) con problemas")
raise SystemExit(0 if total_fallos == 0 else 1)
