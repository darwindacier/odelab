r"""Comprueba que el sitio del laboratorio sirve las tres páginas."""
import time
import urllib.request

BASE = "https://darwindacier.github.io/odelab/"
PAGINAS = {
    "": ["Laboratorio interactivo", "lab01-campos.html", "lab02-resorte-rlc.html"],
    "lab01-campos.html": ["Campos de direcciones", "isoclinas(", "ordenEmpirico"],
    "lab02-resorte-rlc.html": ["Resorte", "diagnosticar", "construirXLSX", "ajusteDecaimiento",
                               "barridoResonancia", "Retrato de fase"],
}

for intento in range(1, 13):
    ok = True
    detalle = []
    for ruta, marcas in PAGINAS.items():
        try:
            with urllib.request.urlopen(
                urllib.request.Request(BASE + ruta, headers={"User-Agent": "verificacion"}),
                timeout=30,
            ) as r:
                html = r.read().decode("utf-8", "replace")
            faltan = [m for m in marcas if m not in html]
            if faltan:
                ok = False
                detalle.append(f"{ruta or 'portada'}: faltan {faltan}")
        except Exception as e:  # noqa: BLE001
            ok = False
            detalle.append(f"{ruta or 'portada'}: {type(e).__name__}")
    if ok:
        print(f"LISTO (intento {intento}): las tres páginas responden y tienen el contenido esperado")
        for ruta, marcas in PAGINAS.items():
            print(f"   ok   /{ruta}  ({len(marcas)} marcas verificadas)")
        break
    print(f"intento {intento}: {'; '.join(detalle)}")
    time.sleep(20)
else:
    print("AVISO: Pages todavía no refleja todo el contenido")
