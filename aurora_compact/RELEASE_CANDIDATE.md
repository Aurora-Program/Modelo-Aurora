# Aurora compacto 0.18.0-rc2

## Contrato candidato

Aurora 0.18.0-rc2 congela una única ley de orientación para la tripleta, la
semilla operativa, el tensor, el diccionario, la ventana y el control:

```text
C[t] → leer K[C] → O[t] = DO[C] → conexión[O] → C[t+1]
```

`C` y `O` no son dos mecanismos. `C` es la orientación que llega a una
relación y `O` es la orientación que esa misma relación entrega. El valor de
`O` entra sin traducción como `C` de la presentación siguiente.

Toda relación produce y conserva una unidad completa:

```text
K = (DO, DE, DS)
```

- `DO` conserva la instrucción de orientación.
- `DE` conserva el conocimiento sobre el cierre de la relación.
- `DS` conserva la información sintetizada.

Ninguno de estos canales es por sí solo «el tensor». Los tres forman el tensor
operativo y los tres pueden actuar como índice para recuperarlo.

## Un diccionario, tres entradas

El diccionario guarda cada `Unit(K)` una sola vez. La orientación recibida
selecciona qué proyección se utiliza como índice:

| `C` | Proyección consultada | Lectura posible |
|---:|---|---|
| `0` | `DO` | instrucción de orientación |
| `1` | `DE` | conocimiento de cierre |
| `2` | `DS` | información sintetizada |

Una coincidencia devuelve siempre el `K` completo y su procedencia. Por tanto,
encontrar una instrucción permite recuperar también su conocimiento y su
información; encontrar una información permite recuperar la instrucción que
la orienta; y encontrar el conocimiento permite reejecutar la relación causal.

Esta tabla describe posiciones de `K`, no tres bases de datos ni tres clases
ontológicas. Las etiquetas expresan lecturas funcionales y pueden adquirir un
papel distinto al formar una relación superior.

Si un índice recupera una unidad, el estado de búsqueda es `1`. Si no recupera
ninguna, es `0`. Si conserva varias candidatas compatibles, es `2` y ninguna se
elimina. La búsqueda exacta sigue realizándose mediante deducción ternaria, no
mediante una igualdad especial del diccionario.

## Emergencia y carry conservan la misma clase de unidad

El candidato no crea un tipo reducido para el carry. Tanto lo que asciende
como lo que continúa es siempre una `Unit(K)` completa, con orientación,
conocimiento, información y procedencia reejecutable.

`DE` tampoco se interpreta de forma aislada. Igual que en el TriGate, primero
se observa el resultado: si `R=2`, la relación permanece abierta aunque `E`
conserve un residual `0` o `1`. Solo una relación cuyo resultado ha dejado de
ser el tensor abierto puede cerrar o contradecirse.

## La ventana como TriGate tensorial

La corrección de `rc2` es que la ventana no agrupa tres tensores ya cerrados.
Replica la forma de la relación mínima y abre el lugar del resultado:

```text
W = (A, B, 2₀)
2₀ = K(222,222,222)
```

La cara ordinaria opera `A` y `B` sobre la posición abierta y hace evolucionar
el tensor `2₀` hasta `2ₑ`. Esa unidad conserva `(A,B,2₀)` como procedencia.
Después solo existen tres transiciones:

| Resultado | Nivel superior | Siguiente ventana |
|---|---|---|
| relación coherente | emergencia `U(A,B,2ₑ)` | comienza desde los siguientes tensores |
| `2ₑ` ambiguo o abierto | — | `(2ₑ, siguiente, 2₀)` |
| relación incoherente | `A` | `(B, siguiente, 2₀)` |

El `2₀` de cada siguiente ventana es una unidad nueva. Por eso una continuación
consume exactamente un tensor nuevo, no dos. El carry conserva todo `K`: en
la apertura es el propio `2ₑ`; en la contradicción es `B`. En la coherencia no
asciende `2ₑ` aisladamente, sino la nueva unidad que emerge de la relación
completa `(A,B,2ₑ)`. En la incoherencia `A` puede ascender individualmente
porque ya constituye la unidad coherente que precede a la composición fallida.
La coherencia exige a la vez cierre relacional y un `2ₑ` ordenable. Una salida
como `012` o `102` no puede emerger aunque `DE` aporte un voto positivo, porque
no admite una orientación no autorreferente.
El `DO` de la unidad retenida se convierte en la fase de la siguiente ventana;
no se reutiliza la orientación del intento que acaba de terminar.

La ventana es así el último paso de una escala. Lo que asciende puede ocupar
`A` o `B` de otra ventana superior; lo que permanece abierto ocupa `A` de la
siguiente ventana del mismo nivel. En ambos casos su `O` entra sin traducción
como `C` de la relación que lo recibe.

## Apertura ternaria

El tercer valor no se convierte automáticamente en una tercera acción. Cuando
la ordenación de una tripleta permanece abierta, se conservan todas sus
orientaciones admisibles. Cuando un puerto abierto contiene las conexiones al
nivel actual y al superior, ambas permanecen disponibles hasta que otra
relación determine el recorrido.

Por tanto:

```text
0 / 1 determinados → una conexión seleccionada
2 abierto           → alternativas estructurales conservadas
```

Los valores concretos de los puertos no poseen universalmente los nombres
«horizontal» y «vertical». Esos efectos proceden de la topología tensorial que
conecta una ventana con otras ventanas.

## Crecimiento fractal

Cada tres unidades almacenadas forman una unidad superior mediante la misma
cara:

```text
9 unidades → 3 unidades emergentes → 1 raíz
```

La raíz conserva todos los descendientes, se reejecuta y puede consultarse por
sus tres canales. No se crean metadatos de prioridad, copias por índice,
contadores, pesos, umbrales ni una ordenación externa.

## Qué queda fuera del candidato

Este RC congela el núcleo estructural, no declara terminado un modelo de
lenguaje ni una red distribuida de producción. Permanecen fuera del contrato:

- la educación lingüística completa;
- la asignación aprendida de topologías entre escalas;
- el protocolo P2P y su seguridad;
- la política ternaria de gasto de ciclos;
- los prototipos históricos de segmentación y competencia basados en acciones
  Python.

Los módulos `growth.py`, `training.py`, `fractal_dictionary.py` y
`output_face.py` se conservan como pruebas históricas y de regresión. El núcleo
candidato está en `fractal_kernel.py` y no depende de sus clasificadores de
movimiento o acción.

## Criterios de aceptación del RC

El candidato será promocionable cuando se mantengan simultáneamente estas
propiedades:

1. toda unidad no hoja se reejecuta desde sus tres descendientes;
2. el mismo `K` se recupera desde `DO`, `DE` y `DS` sin duplicación;
3. `O=DO[C]` se convierte en el siguiente `C` sin tabla de traducción;
4. cambiar únicamente `DE` no cambia la conexión seleccionada;
5. un estado abierto conserva todos los destinos válidos;
6. el crecimiento `1–3–9` usa la misma síntesis y conserva procedencia;
7. el núcleo candidato no despacha acciones semánticas externas;
8. la auditoría finita y la suite de regresión completa permanecen estables.
9. toda ventana nueva tiene exactamente la forma `(A,B,2₀)`;
10. apertura y contradicción consumen un solo tensor siguiente y abren un
    tensor `2₀` nuevo;
11. `R=2` prevalece sobre los residuales de `E` y nunca se descarta como una
    falsa contradicción.
12. `2ₑ` y la emergencia superior son identidades distintas: el primero solo
    continúa cuando permanece ambiguo; la segunda existe únicamente cuando
    la relación `(A,B,2ₑ)` cierra.
13. una salida determinada pero no ordenable, incluidas `012` y `102`, se considera
    incoherente y nunca se fuerza a emerger por un voto aislado de `DE`.

La hipótesis congelada puede resumirse así:

> Toda ventana hace evolucionar una unidad abierta mediante `A` y `B`. Si la
> relación cierra, emerge como unidad superior la composición completa; si
> permanece ambigua, continúa la unidad abierta evolucionada; y si resulta
> incoherente, emerge `A` mientras `B` conserva la continuidad.
