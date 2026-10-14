r"""Comprueba que el sitio sirve el portal y los tres laboratorios."""
import time
import urllib.request

BASE = "https://darwindacier.github.io/odelab/"
PAGINAS = {
    "": ["class=\"pestanas\"", "lab01-campos.html", "lab02-resorte-rlc.html",
         "lab03-tanque-newton-rc.html", "postMessage", "Guía del curso"],
    "lab01-campos.html": ["Campos de direcciones", "ordenEmpirico", "texRender", "data-tex"],
    "lab02-resorte-rlc.html": ["Resorte", "diagnosticar", "construirXLSX", "texRender",
                               "ajusteDecaimiento", "addEventListener('message'"],
    "lab03-tanque-newton-rc.html": ["Tanque de mezclas", "diagnosticar", "estimarTau",
                                    "construirXLSX", "texRender", "addEventListener('message'"],
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
