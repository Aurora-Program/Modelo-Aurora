# Orientación fractal en Aurora 0.17

La orientación no es un metadato añadido a cada escala. Es la misma señal
ternaria observada en dos momentos de una relación:

```text
C[t] → operación → O[t] → C[t+1]
```

`C` es la orientación que recibe la relación. `O` es la orientación que esa
relación conserva y entrega. No tienen por qué ocupar simultáneamente la misma
celda ni poseer el mismo valor, pero no requieren traducción ni un segundo
sistema de control.

## Tripleta

En una tripleta ordenable `P`, `O` selecciona la posición estructural:

```text
ES = P[O]
```

La exclusión de autorreferencia y la fase estable siguen perteneciendo a
`order_triplet()`. La nueva capa no inventa otra tabla de ordenación.

## Relación vertical

Cuando una orientación superior selecciona una de tres relaciones inferiores:

```text
ES↑ = ES[O↑]
```

La misma estructura puede crecer hacia arriba y servir como índice hacia
abajo. La procedencia conserva la relación seleccionada.

## SO y tensor-programa

Una semilla operativa contiene un tensor completo `K=(DO,DE,DS)`. La mayoría
de `DS` expresa la dirección actual `C` y `DO` conserva las orientaciones que
pueden alimentar la relación siguiente. Al compilar un tensor-programa, no se
crea una instrucción distinta: se recupera exactamente ese mismo `K`.

## Ventana

Una ventana abierta ya no produce un objeto reducido `Carry(DE,DO)`. Transporta
la misma unidad completa que produjo la cara:

```text
Carry(Unit(K, descendientes, C, DOt))
```

Por tanto, el carry conserva `DO`, `DE`, `DS`, la dirección, la fotografía
estable y sus tres progenitores. Puede reejecutarse sin reconstrucción.

## Control

Los paquetes finales de `HDS`, `HDE` y `HDO` se vuelven a proyectar como en
cualquier cara:

```text
DOcontrol = (O_HDS, O_HDE, O_HDO)
DEcontrol = (E_HDS, E_HDE, E_HDO)
DScontrol = (R_HDS, R_HDE, R_HDO)
Kcontrol  = (DOcontrol, DEcontrol, DScontrol)
```

Las lecturas llamadas operación, coherencia y alcance son los tres trits de
`DScontrol`; no forman tres estados externos al tensor. `ControlResult`
conserva las tres caras y permite reejecutar causalmente las dos etapas que
producen ese `Kcontrol`.

## Resultado y frontera

La versión 0.17 demuestra que una unidad idéntica puede presentarse desde los
tres índices y que el trit `DO[i]` puede entrar sin traducción como orientación
de la relación siguiente:

```text
C[t+1] = DO[t][i]
```

La elección de `i` sigue perteneciendo a la regla ya congelada de cada escala:
en el diccionario, `C=0` y `C=1` determinan la rama, mientras `C=2` delega la
elección en el orden local. La prueba no asigna todavía un movimiento físico
concreto —ascenso, extensión o desplazamiento— a cada orientación. Esa tabla
solo podrá eliminarse cuando los propios tensores conectados produzcan los
movimientos, sin una acción Python intermedia.
