r"""Valida el laboratorio 03: núcleo afín, los tres fenómenos, el renderizador TeX y el Excel."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "lab03-tanque-newton-rc.html"
TMP = Path(__file__).resolve().parent / "_tmp"
NODE = shutil.which("node") or sys.exit("No se encontró node en el PATH")
XLSX = TMP / "exportado3.xlsx"

script = re.search(r"<script>(.*)</script>", HTML.read_text(encoding="utf-8"), re.S).group(1)
TMP.mkdir(exist_ok=True)
(TMP / "completo3.js").write_text(script, encoding="utf-8")

print("--- sintaxis (node --check) ---")
r = subprocess.run([NODE, "--check", str(TMP / "completo3.js")], capture_output=True, text=True)
print((r.stdout + r.stderr).strip() or "OK")
if r.returncode != 0:
    sys.exit("ERROR DE SINTAXIS")

tex = script[script.index("/* ==== TEX:BEGIN ==== */"):script.index("/* ==== TEX:END ==== */")]
math = script[script.index("/* ==== MATH:BEGIN ==== */"):script.index("/* ==== MATH:END ==== */")]
export = script[script.index("const MIME_XLSX"):script.index("function nombreArchivo")]

pruebas = r"""
const fs = require('fs');
let fallos = 0;
const check = (n, c, extra = "") => {
  console.log((c ? "  ok    " : "  FALLA ") + n + (extra ? "  " + extra : ""));
  if (!c) fallos++;
};
const cerca = (a, b, tol) => Math.abs(a - b) <= tol;

// ---------- 1. Renderizador TeX ----------
const f1 = texRender('\\frac{a}{b}');
check("\\frac produce numerador y denominador", f1.includes('mfrac') && f1.includes('mnum') && f1.includes('mden'));
check("\\sqrt produce radical", texRender('\\sqrt{x}').includes('msqrt'));
check("x^2 produce superíndice", texRender('x^2').includes('<sup>'));
check("c_{in} produce subíndice con dos letras",
      texRender('c_{in}').includes('<sub>') && texRender('c_{in}').includes('in'));
check("\\lambda se convierte en λ en cursiva",
      texRender('\\lambda').includes('λ') && !texRender('\\lambda').includes('class="mr">λ'));
check("las cifras van en redonda", texRender('2x').includes('<span class="mr">2</span>'));
check("\\cos queda en redonda", texRender('\\cos').includes('<span class="mr">cos</span>'));
check("el apóstrofo produce prima", texRender("y'").includes('′'));
check("el menos es el signo tipográfico −", texRender('-x').includes('−'));
check("\\, es un espacio fino", texRender('a\\,b').includes('\u2009'));
check("\\infty produce ∞", texRender('y_\\infty').includes('∞'));
check("\\frac anidado en subíndice", texRender('\\frac{Q}{V}').includes('mfrac'));
check("\\text sale en redonda", texRender('\\text{entrada}').includes('entrada'));
check("llaves equilibradas en una fórmula larga",
      (texRender('A = \\frac{F_0/k}{\\sqrt{(1-r^2)^2 + (2\\zeta r)^2}}').match(/<span/g) || []).length ===
      (texRender('A = \\frac{F_0/k}{\\sqrt{(1-r^2)^2 + (2\\zeta r)^2}}').match(/<\/span>/g) || []).length);
check("no quedan comandos sin traducir",
      !/\\[A-Za-z]+/.test(texRender('\\lambda = \\frac{Q}{V} \\Rightarrow \\tau = \\frac{1}{\\lambda}')));

// ---------- 2. Núcleo afín y los tres fenómenos ----------
const P = { fenomeno: 'tanque', Q: 2, V0: 20, cin: 1, c0: 0, k: 0.05, Tenv: 20, T0: 90,
            R: 10, C: 1, Vf: 10, v0: 0, efecto: 'ninguno',
            fuga: 0.08, kdeg: 0.04, aporte: 0.02, sigma: 1.4, kAmb: 0.02, Rf: 60, Rserie: 12 };

const mt = modeloDe(P);
check("tanque: λ = Q/V y τ = V/Q", cerca(mt.lam, 2 / 20, 1e-12) && cerca(mt.tau, 10, 1e-12));
check("tanque: equilibrio = c_in", cerca(mt.inf, 1, 1e-12));
const mn = modeloDe(Object.assign({}, P, { fenomeno: 'newton' }));
check("newton: τ = 1/k y equilibrio = T_amb", cerca(mn.tau, 20, 1e-12) && cerca(mn.inf, 20, 1e-12));
const mr = modeloDe(Object.assign({}, P, { fenomeno: 'rc' }));
check("rc: τ = RC y equilibrio = V_f", cerca(mr.tau, 10, 1e-12) && cerca(mr.inf, 10, 1e-12));
check("el 63,2 % se alcanza en t = τ",
      cerca(afinSolucion(0.1, 0.1, 0, 10), 0.632 * 1, 1e-3),
      `y(τ)=${afinSolucion(0.1, 0.1, 0, 10).toFixed(4)}`);

// la solución analítica coincide con la integración numérica
let peor = 0;
for (const t of [0.5, 2, 5, 10, 20]) {
  const num = integrarEscalar((x, y) => -mt.lam * y + mt.b, 0, mt.y0, t, 0.001);
  peor = Math.max(peor, Math.abs(num[num.length - 1][1] - afinSolucion(mt.lam, mt.b, mt.y0, t)));
}
check("y(t) analítica = integración numérica (<1e-6)", peor < 1e-6, `peor=${peor.toExponential(2)}`);

// ---------- 3. Estimación de τ desde los datos ----------
const serie = [];
for (let i = 0; i <= 2000; i++) { const t = i * 0.02; serie.push([t, afinSolucion(mt.lam, mt.b, mt.y0, t)]); }
const est = estimarTau(serie, mt.inf, 1);
check("τ estimado de los datos coincide con V/Q",
      est && Math.abs(est.tau - mt.tau) / mt.tau < 0.01, est ? `τ=${est.tau.toFixed(4)}` : "sin ajuste");
check("el ajuste es una recta (R² ≈ 1)", est && est.r2 > 0.999, est ? `R²=${est.r2.toFixed(6)}` : "");

// ---------- 4. Clasificador de efectos en los tres fenómenos ----------
const casos = [
  ['tanque', 'ninguno'], ['tanque', 'fuga'], ['tanque', 'degradacion'], ['tanque', 'aporte'],
  ['newton', 'ninguno'], ['newton', 'ambiente'], ['newton', 'radiacion'],
  ['rc', 'ninguno'], ['rc', 'fuga'], ['rc', 'serie']
];
for (const [fen, ef] of casos) {
  const Q = Object.assign({}, P, { fenomeno: fen, efecto: ef });
  const d = diagnosticar(Q);
  check(`${fen}: detecta «${ef}»`, d.efecto === ef, `dijo «${d.efecto}»`);
}

// ---------- 5. Los efectos cambian de verdad el fenómeno ----------
const mide = (fen, ef, t) => {
  const Q = Object.assign({}, P, { fenomeno: fen, efecto: ef });
  const s = simularReal(Q, t, 0.01);
  return { y: s[s.length - 1][1], extra: s[s.length - 1][2] };
};
check("la fuga baja el volumen", mide('tanque', 'fuga', 60).extra < 0.94 * P.V0);
check("la degradación baja la concentración final",
      mide('tanque', 'degradacion', 200).y < 0.95 * mide('tanque', 'ninguno', 200).y);
check("la radiación enfría más rápido",
      mide('newton', 'radiacion', 5).y < mide('newton', 'ninguno', 5).y,
      `${mide('newton', 'radiacion', 5).y.toFixed(2)} < ${mide('newton', 'ninguno', 5).y.toFixed(2)}`);
check("el ambiente se calienta de verdad",
      mide('newton', 'ambiente', 200).extra > P.Tenv + 1,
      `${mide('newton', 'ambiente', 200).extra.toFixed(2)} °C`);
check("una R de fuga deja el capacitor por debajo de V_f",
      mide('rc', 'fuga', 400).y < 0.95 * P.Vf, `${mide('rc', 'fuga', 400).y.toFixed(3)} V`);

// ---------- 6. Exportación ----------
(async () => {
  const hojas = [
    { nombre: 'Datos', filas: [['t (s)', 'c fenomeno (g/L)', 'c modelo (g/L)'], [0, 0, 0], [1, 0.6, 0.63], [2, 0.86, 0.86]] },
    { nombre: 'Parametros', filas: [['parametro', 'valor'], ['lambda', 0.1], ['tau', 10]] },
    { nombre: 'Metricas', filas: [['metrica', 'valor'], ['discrepancia', 0.4]] },
    { nombre: 'Ajuste', filas: [['t (s)', 'ln|y - y_inf|'], [0, 0], [1, -0.9], [2, -1.9]] }
  ];
  const blob = construirXLSX(hojas);
  const vista = await blob.arrayBuffer();
  fs.writeFileSync(ARCHIVO_XLSX, Buffer.from(vista));
  check("el .xlsx se genera", vista.byteLength > 1500, `${vista.byteLength} bytes`);
  check("firma ZIP correcta", Buffer.from(vista).slice(0, 4).toString('hex') === '504b0304');
  console.log(fallos === 0 ? "\nTODO OK" : `\n${fallos} FALLA(S)`);
  process.exit(fallos === 0 ? 0 : 1);
})();
"""

(TMP / "pruebas3.js").write_text(
    f"const ARCHIVO_XLSX = {str(XLSX)!r};\n" + tex + math + export + pruebas, encoding="utf-8")
print("\n--- aserciones ---")
r2 = subprocess.run([NODE, "--no-warnings", str(TMP / "pruebas3.js")], capture_output=True, text=True)
print(r2.stdout.strip())
if r2.returncode != 0:
    print("stderr:", r2.stderr.strip()[:900])
    sys.exit(r2.returncode)

print("\n--- el .xlsx abierto con openpyxl ---")
from openpyxl import load_workbook  # noqa: E402

wb = load_workbook(XLSX, data_only=True)
ok = wb.sheetnames == ['Datos', 'Parametros', 'Metricas', 'Ajuste']
print(("  ok    " if ok else "  FALLA ") + "cuatro hojas correctas  " + str(wb.sheetnames))
ws = wb['Datos']
ok = ok and ws['A1'].value == 't (s)' and isinstance(ws['B2'].value, (int, float))
print(("  ok    " if ok else "  FALLA ") + f"datos numéricos y encabezado  B2={ws['B2'].value!r}")
sys.exit(0 if ok else 1)
