# El diccionario se orienta fractalmente

Aurora compacto 0.15 prueba que el modo operativo puede convertirse en la
dirección de acceso al diccionario sin introducir una puntuación externa.

El diccionario deja de representarse como una lista ordenada por usos. Es un
bosque ternario. Cada tres programas forman un nodo mediante las mismas nueve
caras que sintetizan cualquier otro tensor-programa:

```text
9 programas observados → 3 programas emergentes → 1 programa raíz
```

El programa emergente conserva los nueve átomos de sus tres descendientes y se
convierte automáticamente en una candidata del nivel siguiente. Esta es la
realimentación: el código aprendido no necesita una llamada especial para
volver al diccionario.

## C es el índice operativo

La misma regla se repite al descender por cada nivel:

```text
C=0, aprendizaje → rama 0
C=1, inferencia  → rama 1
C=2, deducción   → decisión abierta; consulta O
```

`2` no se interpreta como una tercera rama elegida automáticamente. Mantiene
la decisión abierta. El índice se obtiene entonces ordenando el átomo `DO` del
nodo. Ese átomo es la séptima tripleta del tensor-programa:

```text
(I0,I1,I2) | (ODO,ODE,ODS) | (DO,DE,DS)
                                  ↑
                         orden del diccionario
```

No se añade un campo de prioridad. El orden ya forma parte del código.

## El trit superior orienta el nivel inferior

Cuando `O` resuelve una rama, el trit correspondiente del `DO` emergente se
convierte en la fase del nodo inferior. Por tanto, la ruta completa no se
decide de una vez:

```text
C/O raíz → trit superior → C/O nodo → trit superior → programa
```

La operación es autosimilar. Un árbol de nueve hojas ejecuta dos veces la misma
decisión, primero en la raíz y después en uno de sus tres nodos.

En el experimento canónico:

| Consulta | Ruta |
|---|---|
| aprendizaje `C=0` | `0→0` |
| inferencia `C=1` | `1→1` |
| deducción `C=2`, fase `0` | `0→2` |
| deducción `C=2`, fase `2` | `2→2` |

Solo cambia `C` o la orientación heredada; el ejecutor y los nueve programas
permanecen idénticos.

## Apertura honesta

Si `C=2` y el átomo `DO` tampoco posee una ordenación cerrada, la búsqueda no
escoge el primer elemento de una lista. Conserva todos los descendientes del
nodo como alternativas exactas.

Esta regla impide que el orden accidental de Python fabrique una decisión:

```text
C=2 + O abierto → tres ramas todavía disponibles
```

## Realimentación demostrada

Nueve ejecuciones conservan los programas que las produjeron. El diccionario
los refleja y los incorpora en el orden causal observado. Cada terna se
sintetiza; cada tres síntesis vuelven a sintetizarse. Con la experiencia:

```text
A,A,B | A,B,A | B,A,A
```

los tres nodos inferiores producen `A` y la raíz produce nuevamente `A`. Esa
raíz se ejecuta directamente y reproduce la ruta aprendida.

No intervienen `sort`, máximos, soporte, recencia, pesos, umbrales ni un
`reorder()` externo. La recurrencia ocupa una posición superior porque ha
conseguido cerrar dos veces en la estructura `1–3–9`.

## Límite actual

0.15 demuestra una rama completa del diccionario y la promoción ternaria de
programas reflejados. Todavía falta organizar fractalmente varias familias `DS`
simultáneas y hacer que una contradicción contextual realimente `DO` hasta
activar otra raíz sin una nueva consulta del anfitrión.
