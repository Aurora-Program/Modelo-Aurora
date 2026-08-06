# Aurora compacto 0.18.0-rc1

## Contrato candidato

Aurora 0.18.0-rc1 congela una única ley de orientación para la tripleta, la
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

## Emergencia y carry son la misma unidad

El candidato elimina la decisión `DE → movimiento`. `DE` conserva evidencia de
cierre, pero no convierte el resultado en otra clase de objeto.

La ventana contiene tres puertos tensoriales indexados por `O`. La conexión
seleccionada determina dónde se vuelve a presentar la misma unidad:

```text
conexión al nivel actual   → observamos carry
conexión al nivel superior → observamos emergencia
orientación abierta        → se conservan ambos destinos
```

El runtime no contiene acciones denominadas `ASCEND`, `CARRY`, `SHIFT` o
`CRYSTALLIZE`. Solo conserva una topología de tres puertos y entrega el mismo
`Unit(K)` al puerto seleccionado. Carry y emergencia son nombres del recorrido
observado, no formatos de datos ni operaciones fundamentales diferentes.

## La ventana como frontera de escala

Los TriGates producen paquetes `(R,E,O)`. Tres paquetes proyectan
`K=(DO,DE,DS)`. Tres unidades producen otra unidad mediante la misma cara.
Ninguno de esos pasos decide todavía si existe movimiento horizontal o
vertical.

La ventana es el último paso de la escala:

1. recibe tres unidades completas;
2. aplica la cara ordinaria;
3. obtiene otra `Unit(K)` causal y reejecutable;
4. lee `O=DO[C]`;
5. la presenta en la conexión seleccionada;
6. esa orientación entra como `C` de la siguiente relación.

Así, una tripleta, una SO, un tensor, una ventana y un control no imitan la
misma lógica: son presentaciones de la misma operación en escalas diferentes.

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

La hipótesis congelada puede resumirse así:

> Toda operación produce un tensor completo. La orientación decide desde qué
> canal se consulta y en qué conexión vuelve a presentarse. Carry, emergencia,
> conocimiento, información e instrucción son funciones contextuales de la
> misma unidad fractal.
