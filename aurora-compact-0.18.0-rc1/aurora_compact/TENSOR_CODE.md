# Los tensores son el código

Aurora compacto 0.13 prueba una frontera más exigente que 0.12. La dirección
de la cara ya no es el único elemento tensorial: la presentación completa se
expresa mediante un tensor de nueve tripletas.

```text
(I0, I1, I2) | (ODO, ODE, ODS) | (DO, DE, DS)
```

- `I0..I2` son las tres direcciones de celda que se presentan a la cara.
- `ODO..ODS` son las direcciones donde se publican sus tres canales.
- `DO` es la fase estable.
- `DE=111` indica que la instrucción está cerrada.
- La firma homogénea `DS=(C,C,C)` selecciona la dirección de la cara.

Las direcciones de celda son también tripletas Aurora. El compilador no
contiene categorías semánticas: únicamente lee las nueve posiciones, crea las
seis referencias y entrega la instrucción al ejecutor relacional 0.12. Cambiar
una dirección dentro del tensor cambia el recorrido sin modificar el runtime.

## Por qué `DE` forma parte del código

`DS=222` tiene dos lecturas posibles: apertura o dirección `C=2`. Un código no
puede decidirlo observando `DS` de forma aislada. La instrucción canónica usa
`DE=111` para expresar que la relación instructiva ha cerrado. De este modo:

```text
DE=111, DS=000 -> aprender M
DE=111, DS=111 -> inferir R
DE=111, DS=222 -> deducir B
```

Un tensor completamente abierto `DE=222, DS=222` continúa sin determinar una
dirección ejecutable.

## Inducción de código sin contador

Tres programas candidatos se alinean por sus nueve posiciones. Cada posición
entra en una cara Aurora ordinaria. El resultado son nueve unidades nuevas,
cada una con los tres programas candidatos como procedencia reejecutable.

En la prueba principal:

```text
A, A, B -> A
```

Las dos experiencias coincidentes sintetizan de nuevo el programa `A`. El
programa emergente se entrega al mismo ejecutor y reproduce la ruta de `A`.
No se calcula soporte, frecuencia, peso, distancia, umbral ni `max()`.

La prueba contraria presenta tres programas cuya dirección de salida produce
el tensor imposible `102`. Las tres hipótesis se conservan, pero la síntesis no
se ejecuta como programa. Aurora no fabrica un ganador cuando la relación no
ha cerrado.

## Qué se ha demostrado

1. Entradas, salidas, fase y operación pueden vivir en un tensor ordinario.
2. Cambiar solo ese tensor cambia el comportamiento del ejecutor.
3. Una relación entre programas puede producir otro programa reejecutable.
4. El programa producido puede ejecutarse sin una acción Python especializada.
5. La ausencia de cierre conserva las alternativas y bloquea la ejecución.

## Extensión 0.14

La procedencia de una ventana ya produce los programas candidatos y los vuelve
a presentar al mismo circuito de inducción. Cada semilla conserva las nueve
unidades que la originaron; el disparo las refleja, verifica que corresponden
a las entradas, salidas e instrucción ejecutadas y las agrupa únicamente con
experiencias de la misma ventana causal.

## Extensión 0.15

Los programas reflejados se promueven ahora en el mismo patrón `1–3–9`: tres
programas producen un nodo y tres nodos producen una raíz ejecutable. La
posición `DO` del tensor-programa orienta el descenso cuando `C=2` conserva la
decisión abierta. Véanse `PROVENANCE_CODE.md` y `FRACTAL_DICTIONARY.md`.

## Extensión 0.16

La cara de salida usa esos programas como requisitos de tres búsquedas
paralelas. Si dos búsquedas cierran y una ausencia queda determinada, el
diccionario incorpora exactamente el tensor-programa de salida que ya existe.
No llama a `author()` durante la resolución. Véase `OUTPUT_FACE.md`.
