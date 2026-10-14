# Laboratorio de Ecuaciones Diferenciales

Laboratorios interactivos para la asignatura **Ecuaciones Diferenciales (O2017216)** de la
Licenciatura en Matemáticas, Universidad del Magdalena. Cada laboratorio enfrenta un **fenómeno
físico manipulable** con su **modelo matemático**, mide la diferencia entre ambos y permite
descargar los datos para analizarlos en Excel.

Sitio publicado: https://darwindacier.github.io/odelab/

## Laboratorios

| # | Tema | Qué se manipula | Verificación |
|---|------|-----------------|--------------|
| 01 | Campos de direcciones, isóclinas y métodos numéricos | `f(x, y)` escrita por el estudiante, paso `h`, condiciones iniciales | error global y orden empírico de Euler, Heun y RK4 medidos contra la solución exacta |
| 02 | Resorte–masa–amortiguador y circuito RLC | `m/L`, `c/R`, `k/(1/C)`, `F₀/V₀`, `ω`, condiciones iniciales | el fenómeno simulado contra el modelo lineal: discrepancia, RMS y clasificación del efecto no modelado |
| 03 | Tanque de mezclas, enfriamiento de Newton y circuito RC | caudales, concentración de entrada, `k`, temperaturas, `R` y `C` | valor final y τ medidos contra el modelo; clasificador de fuga, degradación, aporte, radiación y resistencia extra |
| 04 | Sistemas, plano de fase y estabilidad | matrices 2×2, modelos depredador–presa | *(en preparación)* |

## Qué hace especiales a estos laboratorios

1. **Fenómeno y modelo en la misma pantalla.** No es una animación: el fenómeno se integra con
   Runge–Kutta de cuarto orden y el modelo se integra en paralelo con las mismas condiciones y la
   misma excitación, de modo que la curva de diferencia es una medición real de lo que el modelo
   no explica.
2. **Efectos ocultos y diagnóstico.** El laboratorio 02 puede activar tres efectos que el modelo
   lineal no contempla (rozamiento seco, resorte no lineal, amortiguamiento cuadrático). Un
   clasificador numérico los detecta a partir del decaimiento libre y del corrimiento del pico de
   resonancia, y el estudiante debe diagnosticarlos observando las gráficas.
3. **Gráficas manipulables.** Zoom con la rueda, desplazamiento temporal arrastrando, series
   conmutables, cursor de lectura, retrato de fase, balance de energía y ajuste exponencial que
   estima ζ desde los propios datos.
4. **Datos para Excel.** Cada laboratorio exporta un `.xlsx` con varias hojas (datos, parámetros,
   métricas y barrido de resonancia) y un CSV con separador `;` y coma decimal, listo para Excel en
   español.
5. **Autónomos y sin dependencias.** Un solo archivo HTML por laboratorio, sin librerías, sin
   servidor y sin conexión después de la primera carga. Funcionan en computador y en móvil. Las
   fórmulas se componen con un pequeño renderizador LaTeX propio (fracciones, raíces, subíndices,
   letras griegas), de modo que se leen como matemáticas sin cargar KaTeX ni MathJax.

## Uso en el aula

Predicción → manipulación → comparación con el modelo → descarga de datos y ajuste en Excel →
diagnóstico del supuesto que falla. Encaja como laboratorio de clase, como trabajo autónomo en
lunes festivos o como material de estudio antes del examen.

## Interfaz

- **Guía de entrada** la primera vez que se abre cada laboratorio (se puede desactivar y reabrir con
  el botón *Guía*).
- **Globos de ayuda** en cada tarjeta, con la explicación de qué hace y qué mirar.
- **Panel lateral plegable** para dejar más espacio a las gráficas, y **pausa** de la simulación.
- **Chips de estado** en la cabecera: los parámetros derivados y la discrepancia, que cambia de
  color cuando el modelo se aleja de lo medido.
- **Comparadores visuales** de barras entre el valor medido y el del modelo.
- **Avisos emergentes** al exportar, al pausar y al superar un reto.
- **Atajos:** `espacio` pausa, `R` reinicia, `P` pliega el panel, `G` guarda el PNG, `Esc` cierra la guía.
- **Gráficas con ejes reales:** marcas numeradas, cuadrícula, unidades, leyenda y recuadros de lectura.
  Rueda: zoom anclado al puntero · arrastrar: desplazar · doble clic: vista completa.
- **Campo de direcciones:** clic lanza una curva, arrastrar desplaza la vista (también en pantallas táctiles)
  y el puntero muestra `x`, `y` y la pendiente `f(x, y)`.
- Diseño adaptable: en pantallas estrechas las gráficas y el panel se apilan.

## Verificación técnica

Antes de publicar, cada laboratorio pasa una batería de aserciones numéricas ejecutada con Node
(los scripts de `validacion/` buscan `node` en el PATH y se pueden ejecutar desde cualquier carpeta;
por ejemplo, que la solución analítica coincida con la integración numérica, que el orden empírico
de cada método sea el teórico, que la energía se conserve sin amortiguamiento y que el clasificador
identifique correctamente los cuatro casos). El archivo `.xlsx` exportado se abre y se revisa con
openpyxl y con el verificador estructural de paquetes Office.

## Créditos

**Dr. Darwin Peña González** — Departamento de Matemáticas y Estadística, Universidad del Magdalena.
Licencia MIT (ver `LICENSE`).
