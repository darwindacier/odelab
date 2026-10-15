# Laboratorio de Ecuaciones Diferenciales

Laboratorios interactivos para la asignatura **Ecuaciones Diferenciales (O2017216)** de la
Licenciatura en Matemáticas, Universidad del Magdalena. Cada laboratorio enfrenta un **fenómeno
físico manipulable** con su **modelo matemático** y mide la diferencia entre ambos; los
laboratorios 02 y 03 permiten además descargar los datos para analizarlos en Excel.

Sitio publicado: https://darwindacier.github.io/odelab/

## Laboratorios

| # | Tema | Qué se manipula | Verificación |
|---|------|-----------------|--------------|
| 01 | Campos de direcciones, isóclinas y métodos numéricos | `f(x, y)` escrita por el estudiante, paso `h`, condiciones iniciales | error global y orden empírico de Euler, Heun y RK4, medidos contra la solución exacta o, si no se conoce, contra una referencia RK4 de paso fino |
| 02 | Resorte–masa–amortiguador y circuito RLC | `m/L`, `c/R`, `k/(1/C)`, `F₀/V₀`, `ω`, condiciones iniciales | el fenómeno simulado contra el modelo lineal: discrepancia, RMS y clasificación del efecto no modelado |
| 03 | Tanque de mezclas, enfriamiento de Newton y circuito RC | caudales, concentración de entrada, `k`, temperaturas, `R` y `C` | valor final y τ medidos contra el modelo; clasificador de fuga, degradación, aporte, ambiente que cambia, radiación y resistencia extra |
| 04 | Sistemas, plano de fase y estabilidad | matrices 2×2, modelos depredador–presa | *(en preparación)* |

El portal (`index.html`) reúne los tres laboratorios en pestañas y trae una guía del curso con la
correspondencia entre el modelo general y cada fenómeno.

## Qué hace especiales a estos laboratorios

1. **Fenómeno y modelo en la misma pantalla.** No es una animación: el fenómeno se integra con
   Runge–Kutta de cuarto orden y el modelo se integra en paralelo con las mismas condiciones y la
   misma excitación, de modo que la curva de diferencia es una medición real de lo que el modelo
   no explica.
2. **Efectos ocultos y diagnóstico.** Los laboratorios 02 y 03 pueden activar efectos que el
   modelo no contempla. En el 02 son rozamiento seco, resorte que se ablanda y amortiguamiento
   cuadrático; un clasificador numérico suelta el sistema sin excitación y los distingue por la
   rigidez medida al soltarlo, la duración del primer medio ciclo, si la masa se queda quieta
   fuera del equilibrio y la forma del decaimiento. En el 03 son fuga, degradación, aporte, un
   ambiente que cambia, radiación y resistencias extra; el clasificador integra hasta el equilibrio
   real y compara el valor final y τ con el modelo. En **modo examen** el efecto se elige al azar y
   queda oculto (también en el selector, el veredicto y los archivos exportados) hasta que el
   estudiante da su diagnóstico.
3. **Gráficas manipulables.** Zoom con la rueda, desplazamiento temporal arrastrando, series
   conmutables, cursor de lectura, retrato de fase, balance de energía y ajustes que estiman los
   parámetros desde los propios datos: ζ con la recta de `ln Aₙ` contra el instante `tₙ` de cada
   pico (laboratorio 02) y τ con la recta de `ln|y − y∞|` contra `t` (laboratorio 03).
4. **Datos para Excel.** Los laboratorios 02 y 03 exportan un `.xlsx` con varias hojas (datos,
   parámetros, métricas, y el barrido de resonancia o el ajuste de τ) y un CSV con separador `;` y
   coma decimal, listo para Excel en español. También guardan PNG de las gráficas y del fenómeno.
5. **Autónomos y sin dependencias.** Un solo archivo HTML por laboratorio, sin librerías, sin
   servidor y sin conexión después de la primera carga. Funcionan en computador y en móvil. Las
   fórmulas se componen con un pequeño renderizador LaTeX propio (fracciones, raíces, subíndices,
   letras griegas), de modo que se leen como matemáticas sin cargar KaTeX ni MathJax.

## Uso en el aula

Predicción → manipulación → comparación con el modelo → descarga de datos y ajuste en Excel →
diagnóstico del supuesto que falla. Encaja como laboratorio de clase, como trabajo autónomo en
lunes festivos o como material de estudio antes del examen.

## Interfaz

- **Guía de entrada** en el botón *Guía* de cada laboratorio; se abre sola la primera vez cuando el
  laboratorio se abre suelto (dentro del portal no, para no tapar la pestaña).
- **Globos de ayuda** en cada tarjeta, con la explicación de qué hace y qué mirar.
- **Panel lateral plegable** para dejar más espacio a las gráficas, y **pausa** de la simulación.
- **Chips de estado** en la cabecera: los parámetros derivados y la discrepancia, que cambia de
  color cuando el modelo se aleja de lo medido.
- **Comparadores visuales** de barras entre el valor medido y el del modelo.
- **Avisos emergentes** al exportar, al pausar y al superar un reto.
- **Atajos:** en los laboratorios 02 y 03, `espacio` pausa, `R` reinicia, `P` pliega el panel y
  `G` guarda el PNG; en el 01, `R` borra las curvas y `P` pliega el panel; `Esc` cierra la guía.
- **Gráficas con ejes reales:** marcas numeradas, cuadrícula, unidades, leyenda y recuadros de lectura.
  Rueda: zoom anclado al puntero · arrastrar: desplazar · doble clic: vista completa.
- **Campo de direcciones:** clic lanza una curva, arrastrar desplaza la vista (también en pantallas táctiles)
  y el puntero muestra `x`, `y` y la pendiente `f(x, y)`. Si la solución deja de existir antes del
  final del intervalo (por ejemplo, `y' = −x/y` al llegar a `y = 0`), la comparación se acorta sola.
- **Reloj adaptado a τ** en el laboratorio 03: el camino completo al equilibrio se ve en unos
  segundos, sea τ de una décima de segundo o de varios minutos.
- **Portal con pestañas:** cada pestaña conserva su estado y la que no se ve queda en pausa;
  `←` y `→` cambian de pestaña, `F` pone pantalla completa, cada pestaña tiene su propio enlace y
  los atajos de los laboratorios funcionan justo después de cambiar de pestaña.
- Diseño adaptable: en pantallas estrechas las gráficas y el panel se apilan, y las tablas de la
  guía se desplazan en horizontal.

## Verificación técnica

Antes de publicar, cada laboratorio pasa una batería de aserciones numéricas ejecutada con Node.
Los scripts de `validacion/` buscan `node` en el PATH y se pueden ejecutar desde cualquier carpeta.

| Script | Qué comprueba |
|--------|---------------|
| `validar-lab01.py` | parser de expresiones, soluciones exactas del catálogo, campo e isóclinas, orden empírico con el `h` del estudiante, métodos exactos sin orden medible, referencia fina y detección del dominio de la solución |
| `validar-lab02.py` | amplitud y resonancia teóricas contra la integración, solución analítica, conservación de la energía (también del resorte no lineal), clasificador con `F₀ = 0` y en los tres regímenes, barrido de 432 casos sin efectos inventados ni confundidos, resorte no lineal acotado, adherencia del rozamiento seco y exportación a Excel |
| `validar-lab03.py` | renderizador TeX, núcleo afín y los tres fenómenos, estimación de τ, clasificador con un barrido por los rangos de los deslizadores, tanque que se vacía, radiación en kelvin, equilibrio de Newton y exportación a Excel |
| `validar-formulas.py` | que todas las fórmulas `data-tex` se compongan bien |
| `auditar-interfaz.py` | identificadores, ayudas y estructura de cada laboratorio |
| `auditar-portal.py` | pestañas, archivos enlazados y mensajes entre el portal y los laboratorios |
| `verificar-sitio.py` | que el sitio publicado sirva el portal y los tres laboratorios |

Los validadores de cada laboratorio revisan además el contenido de la página, para que no vuelvan
errores de interfaz ya corregidos. El archivo `.xlsx` exportado se abre y se revisa con openpyxl.

## Cambios recientes

**15 de octubre de 2026**

- **Laboratorio 01.** Los botones *Guía* y *No volver a mostrarla* dejaban el campo en blanco. El
  reto ahora se verifica en cualquier ecuación, también la que escribe el estudiante; *Aplicar*
  conserva la solución exacta de las ecuaciones del catálogo; el orden empírico usa el `h` elegido,
  marca como *exacto* el método que no comete error (Heun y RK4 en `y' = 2x`) y el intervalo por
  defecto ya no es simétrico, lo que hacía aparentar orden 2 a Euler en `y' = cos x`.
- **Laboratorio 02.** El clasificador ya no confunde el modelo lineal con un resorte no lineal
  cuando `F₀ = 0` o en los regímenes crítico y sobreamortiguado. El resorte que se ablanda es ahora
  `k x/(1 + a x²)`, que no diverge, y el rozamiento seco deja la masa quieta en lugar de vibrar. El
  ajuste de ζ usa `ln Aₙ` contra `tₙ`, el amortiguamiento llega hasta 60 para que el botón
  *Crítico* funcione con cualquier `m` y `k`, la historia guarda 20 s y el circuito RLC usa C y A.
- **Laboratorio 03.** *Ir al equilibrio* ya no enfría la taza en Newton, la radiación se calcula en
  kelvin, el tanque con fuga se vacía y se detiene, y el clasificador integra hasta el equilibrio
  real, de modo que una resistencia en serie ya no se confunde con una fuga.
- **Modo examen** en los laboratorios 02 y 03: el efecto queda oculto de verdad y se puede salir.
- **Portal.** Atajos dentro de las pestañas y guía del curso corregida: notación `a₂ y'' + a₁ y' + a₀ y`
  y tabla del modelo de primer orden del laboratorio 03.
- **Licencia.** Aviso MIT en la cabecera de cada archivo y enlace en el pie del portal.

## Créditos

**Dr. Darwin Peña González** — Departamento de Matemáticas y Estadística, Universidad del Magdalena.
Licencia MIT (ver `LICENSE`); cada archivo lleva el aviso de copyright en su cabecera.
