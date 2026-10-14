r"""Valida el laboratorio ODE 01: sintaxis y matemática (parser, campo, isóclinas, órdenes)."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "lab01-campos.html"
TMP = Path(__file__).resolve().parent / "_tmp"
NODE = shutil.which("node") or sys.exit("No se encontró node en el PATH")

script = re.search(r"<script>(.*)</script>", HTML.read_text(encoding="utf-8"), re.S).group(1)
TMP.mkdir(exist_ok=True)
(TMP / "completo.js").write_text(script, encoding="utf-8")

print("--- sintaxis (node --check) ---")
r = subprocess.run([NODE, "--check", str(TMP / "completo.js")], capture_output=True, text=True)
print((r.stdout + r.stderr).strip() or "OK")
if r.returncode != 0:
    sys.exit("ERROR DE SINTAXIS")

math = script[script.index("/* ==== MATH:BEGIN ==== */"):script.index("/* ==== MATH:END ==== */")]

pruebas = r"""
let fallos = 0;
const check = (n, c, extra = "") => {
  console.log((c ? "  ok    " : "  FALLA ") + n + (extra ? "  " + extra : ""));
  if (!c) fallos++;
};
const cerca = (a, b, tol) => Math.abs(a - b) <= tol;

// ---------- 1. Parser ----------
const ev = (src, x, y) => compilarExpresion(src)(x, y);
check("precedencia 2+3*4 = 14", ev("2+3*4", 0, 0) === 14);
check("potencia a la derecha 2^3^2 = 512", ev("2^3^2", 0, 0) === 512);
check("menos unario -x^2 en x=3 = -9", ev("-x^2", 3, 0) === -9);
check("paréntesis (-x)^2 en x=3 = 9", ev("(-x)^2", 3, 0) === 9);
check("funciones sin(pi/2) = 1", cerca(ev("sin(pi/2)", 0, 0), 1, 1e-12));
check("raíz sqrt(x^2+y^2) en (3,4) = 5", cerca(ev("sqrt(x^2+y^2)", 3, 4), 5, 1e-12));
check("división 1/x en x=4 = 0.25", ev("1/x", 4, 0) === 0.25);
check("logaritmo exp(ln(5)) = 5", cerca(ev("exp(ln(5))", 0, 0), 5, 1e-12));
check("constante e^x en x=1 = e", cerca(ev("e^x", 1, 0), Math.E, 1e-12));
const fallaBien = (src) => { try { compilarExpresion(src); return false; } catch (e) { return true; } };
check("rechaza «x +»", fallaBien("x +"));
check("rechaza «foo(2)»", fallaBien("foo(2)"));
check("rechaza «x@2»", fallaBien("x@2"));
check("rechaza «(x»", fallaBien("(x"));
check("rechaza «sin x»", fallaBien("sin x"));

// ---------- 2. Catálogo: cada solución exacta satisface la ecuación ----------
for (const c of CATALOGO) {
  const f = compilarExpresion(c.expr);
  if (!c.exacta) { check(`${c.expr}: invariante presente`, typeof c.invariante === "function"); continue; }
  let peor = 0;
  const x0 = 0.3, y0 = 0.7;
  for (let i = 1; i <= 40; i++) {
    const x = x0 + i * 0.02, d = 1e-6;
    const der = (c.exacta(x + d, x0, y0) - c.exacta(x - d, x0, y0)) / (2 * d);
    peor = Math.max(peor, Math.abs(der - f(x, c.exacta(x, x0, y0))));
  }
  check(`${c.expr}: la solución exacta cumple y' = f`, peor < 1e-5, `defecto=${peor.toExponential(2)}`);
}

// ---------- 3. Campo de direcciones ----------
const fCampo = compilarExpresion("x + y");
const campo = campoDirecciones(fCampo, -4, 4, -3, 3, 21, 15);
check("campo: nx*ny puntos", campo.length === 21 * 15, String(campo.length));
const enOrigen = campo.find(p => p.x === 0 && p.y === 0);
check("campo en (0,0) para y'=x+y: dirección (1,0)", cerca(enOrigen.m, 0, 1e-12) && cerca(enOrigen.ux, 1, 1e-12));
const bienNormalizado = campo.every(p => cerca(Math.hypot(p.ux, p.uy), 1, 1e-9));
check("campo: direcciones unitarias", bienNormalizado);
const conSingularidad = campoDirecciones(compilarExpresion("sqrt(y)"), -1, 1, -1, 1, 9, 9);
check("campo: omite puntos no finitos (sqrt(y) con y<0)", conSingularidad.every(p => p.y >= 0));

// ---------- 4. Isóclinas ----------
// Para y' = x + y, la isóclina f = k es la recta y = k - x.
const iso = isoclinas(fCampo, 0, -4, 4, -3, 3, 90);
const desvio = iso.reduce((m, s) => Math.max(m, ...s.map(p => Math.abs(p[1] + p[0]))), 0);
check("isóclina k=0 de y'=x+y es la recta y=-x", iso.length > 50 && desvio < 0.05,
      `segmentos=${iso.length} desvío=${desvio.toFixed(4)}`);
const iso2 = isoclinas(fCampo, 2, -4, 4, -3, 3, 90);
const desvio2 = iso2.reduce((m, s) => Math.max(m, ...s.map(p => Math.abs(p[1] + p[0] - 2))), 0);
check("isóclina k=2 es la recta y=2-x", desvio2 < 0.05, `desvío=${desvio2.toFixed(4)}`);

// ---------- 5. Métodos: orden empírico ----------
const fExp = compilarExpresion("y");
const exactaExp = (x, x0, y0) => y0 * Math.exp(x - x0);
const ordenes = {};
for (const m of ["euler", "heun", "rk4"]) {
  ordenes[m] = ordenEmpirico(fExp, 0, 1, 1, x => exactaExp(x, 0, 1), m);
}
check("Euler tiene orden ≈ 1", cerca(ordenes.euler, 1, 0.15), `orden=${ordenes.euler.toFixed(3)}`);
check("Heun tiene orden ≈ 2", cerca(ordenes.heun, 2, 0.2), `orden=${ordenes.heun.toFixed(3)}`);
check("RK4 tiene orden ≈ 4", cerca(ordenes.rk4, 4, 0.25), `orden=${ordenes.rk4.toFixed(3)}`);

// ---------- 6. Integración ----------
const ptsRK = integrar(compilarExpresion("2*x"), 0, 1, 3, 0.1, "rk4");
check("RK4 es exacto en y'=2x (polinomio de grado 2)",
      cerca(ptsRK[ptsRK.length - 1][1], 1 + 9, 1e-12), `y(3)=${ptsRK[ptsRK.length - 1][1]}`);
const errH = [0.2, 0.1, 0.05, 0.025].map(h => {
  const p = integrar(fExp, 0, 1, 1, h, "euler");
  return Math.abs(p[p.length - 1][1] - Math.E);
});
check("el error de Euler baja al reducir h", errH.every((e, i) => i === 0 || e < errH[i - 1]),
      errH.map(e => e.toFixed(4)).join(" > "));
const haciaAtras = integrar(fExp, 1, Math.E, 0, 0.05, "rk4");
check("integra hacia atrás (de x=1 a x=0)", cerca(haciaAtras[haciaAtras.length - 1][1], 1, 1e-6),
      `y(0)=${haciaAtras[haciaAtras.length - 1][1]}`);

// ---------- 7. Comportamiento cualitativo ----------
const fLog = compilarExpresion("y*(1 - y)");
const alUno = (y0) => {
  const p = integrar(fLog, 0, y0, 25, 0.05, "rk4");
  return p[p.length - 1][1];
};
check("logístico: y0=0.9 tiende a 1", cerca(alUno(0.9), 1, 1e-6), `y(25)=${alUno(0.9)}`);
check("logístico: y0=1.1 tiende a 1", cerca(alUno(1.1), 1, 1e-6), `y(25)=${alUno(1.1)}`);
check("logístico: y0=1 se queda en 1 (equilibrio)", cerca(alUno(1), 1, 1e-9));
check("logístico: y0=0 se queda en 0 (equilibrio)", cerca(alUno(0), 0, 1e-12));

const fCirc = compilarExpresion("-x/y");
const circ = integrar(fCirc, 0, 1, 0.9, 0.001, "rk4");
const inv = Math.max(...circ.map(([x, y]) => Math.abs(x * x + y * y - 1)));
check("y'=-x/y conserva x²+y²=1 (invariante)", inv < 1e-6, `desvío=${inv.toExponential(2)}`);

// ---------- 8. Defecto ----------
const exactos = [];
for (let i = 0; i <= 2000; i++) { const x = i / 2000; exactos.push([x, Math.exp(x)]); }
check("defecto de la solución exacta ≈ 0", defectoMaximo(fExp, exactos) < 1e-5,
      defectoMaximo(fExp, exactos).toExponential(2));
const eulerPts = integrar(fExp, 0, 1, 1, 0.2, "euler");
check("defecto de Euler con h=0.2 es apreciable", defectoMaximo(fExp, eulerPts) > 1e-3,
      defectoMaximo(fExp, eulerPts).toExponential(2));

console.log(fallos === 0 ? "\nTODO OK" : `\n${fallos} FALLA(S)`);
process.exit(fallos === 0 ? 0 : 1);
"""

(TMP / "pruebas.js").write_text(math + pruebas, encoding="utf-8")
print("\n--- aserciones ---")
r2 = subprocess.run([NODE, str(TMP / "pruebas.js")], capture_output=True, text=True)
print(r2.stdout.strip())
if r2.returncode != 0:
    print("stderr:", r2.stderr.strip()[:800])
sys.exit(r2.returncode)


