r"""Comprueba que todas las fórmulas data-tex de los laboratorios se componen bien."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(r"C:\Users\Darwin\Desktop\odelab")
TMP = Path(r"C:\Users\Darwin\Desktop\_val_ode")
NODE = r"C:\Users\Darwin\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe"
LABS = ["lab01-campos.html", "lab02-resorte-rlc.html", "lab03-tanque-newton-rc.html"]

TMP.mkdir(exist_ok=True)
total = 0
fallos = 0

for lab in LABS:
    texto = (BASE / lab).read_text(encoding="utf-8")
    script = re.search(r"<script>(.*)</script>", texto, re.S).group(1)
    tex = script[script.index("/* ==== TEX:BEGIN ==== */"):script.index("/* ==== TEX:END ==== */")]

    # fórmulas escritas en el HTML y fórmulas construidas en el código (con \\)
    del_html = re.findall(r'data-tex="([^"]*)"', texto)
    del_js = [m.replace("\\\\", "\\") for m in re.findall(r'data-tex=\\\\?"((?:[^"\\]|\\.)*?)\\\\?"', script)]

    formulas = sorted(set(del_html + del_js))
    total += len(formulas)

    pruebas = r"""
let fallos = 0;
const formulas = FORMULAS;
for (const f of formulas) {
  const html = texRender(f);
  const problemas = [];
  if (/\\[A-Za-z]+/.test(html)) problemas.push('comando sin traducir');
  if ((html.match(/<span/g) || []).length !== (html.match(/<\/span>/g) || []).length) problemas.push('span desbalanceado');
  if ((html.match(/<sup>/g) || []).length !== (html.match(/<\/sup>/g) || []).length) problemas.push('sup desbalanceado');
  if ((html.match(/<sub>/g) || []).length !== (html.match(/<\/sub>/g) || []).length) problemas.push('sub desbalanceado');
  if (!html.trim()) problemas.push('vacío');
  if (/[{}]/.test(html)) problemas.push('llaves visibles');
  if (problemas.length) { console.log('  FALLA ' + f + '  -> ' + problemas.join(', ')); fallos++; }
}
console.log(fallos === 0 ? `  ok    ${formulas.length} fórmulas compuestas sin problemas`
                         : `  ${fallos} de ${formulas.length} con problemas`);
process.exit(fallos === 0 ? 0 : 1);
"""
    (TMP / "tex_prueba.js").write_text(
        f"const FORMULAS = {json.dumps(formulas, ensure_ascii=False)};\n" + tex + pruebas,
        encoding="utf-8")
    r = subprocess.run([NODE, "--no-warnings", str(TMP / "tex_prueba.js")],
                       capture_output=True, text=True)
    print(f"=== {lab} ===")
    print(r.stdout.strip() or r.stderr.strip()[:400])
    if r.returncode != 0:
        fallos += 1

print(f"\nTOTAL: {total} fórmulas revisadas en {len(LABS)} laboratorios · "
      + ("todas correctas" if fallos == 0 else f"{fallos} laboratorio(s) con fallos"))
sys.exit(0 if fallos == 0 else 1)
