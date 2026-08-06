# Perfil ejecutable Aurora 0.18.0-rc1

Este perfil conserva la separación 0.12 entre el núcleo universal y los
comportamientos que deben llegar mediante educación. Ante una diferencia con
perfiles anteriores, las reglas release candidate de este documento prevalecen.

## Núcleo congelado

1. El vocabulario es `{0,1,2}` y `Majority3(0,1,2)=2`.
2. Las direcciones son `0=aprender M`, `1=inferir R`, `2=deducir B`.
3. `E` conserva el residual único cuando el resultado mayoritario es `2`; en
   los demás casos clasifica el dominio dirigido como cierre, contradicción o
   apertura.
4. Una cara ordena, entrelaza tres TriGates, proyecta canales homólogos y
   produce `K=(DO,DE,DS)`.
5. C4 opera `DS`, C5 opera `DE` y C6 opera `DO` de entrada, conocimiento y
   salida. Cada una vuelve a ser una cara ordinaria.
6. `012`, `111` y `000` pueden aparecer como firmas o propósitos, pero el
   núcleo no calcula distancias externas contra ellas.
7. La búsqueda ejecuta deducción sobre `B`; conserva el dominio completo y no
   confunde el trit literal `2` con un conjunto de candidatas.
8. Una unidad conserva `K`, dirección, fase y los tres descendientes que la
   produjeron. Toda unidad no hoja debe poder reejecutarse.
9. Un token simple usa `DO=222`, `DE=222` y su `DS` explícito. Más de un tensor
   puede representar el mismo token sin que uno borre al otro.

La convención canónica de esta rama es `0=aprender M`, `1=inferir R` y
`2=deducir B`. Cualquier tabla anterior que intercambie `0` y `2` queda
obsoleta. La lógica del TriGate, la ordenación y la cara permanece congelada;
0.17 completó la identidad del carry y la proyección superior del control;
0.18.0-rc1 congela el paso por conexiones orientadas y los tres índices de `K`.

## Ejecutor relacional universal

10. Una semilla operativa es una `Unit`, no una función especializada. La
    mayoría de su canal `DS` determina `C` y su canal `DO` contiene la fase que
    leerá la cara.
11. La educación contiene únicamente semillas y conexiones entre celdas. Cada
    semilla declara tres celdas de entrada y tres celdas de salida para
    `DO`, `DE` y `DS`.
12. Cuando las tres entradas de una semilla están disponibles, el ejecutor
    aplica `face()` y publica sus tres canales. Una celda nueva reactiva las
    semillas que dependen de ella.
13. El ejecutor no interpreta el significado de las direcciones, de las
    celdas ni de los canales. Tampoco contiene acciones llamadas ascenso,
    carry, desplazamiento, segmentación, poda o sílaba.
14. Una salida solo cambia el comportamiento por la forma en que la educación
    vuelva a presentarla. Conectar tres `DS` inferiores a otra semilla produce
    lo que observamos como ascenso; conectar un `DS` abierto con dos entradas
    posteriores produce lo que observamos como carry.
15. Todas las combinaciones exactas de señales presentes en las tres celdas se
    ejecutan. El runtime no usa `max()`, soporte, recencia, anchura, pesos ni
    umbrales para borrar alternativas.
16. Cada señal emitida conserva la semilla, el canal, el conocimiento completo
    y las tres señales progenitoras. La traza entera debe reejecutarse mediante
    la cara congelada.
17. Una combinación exacta de semilla y tres señales se ejecuta una sola vez.
    El sistema se detiene al alcanzar un punto fijo local o al agotar el gasto
    explícito asignado a una educación cíclica.
18. La educación se serializa como JSON de tensores y conexiones, sin callbacks
    ni código Python. Cambiar ese documento puede cambiar la operación sin
    modificar el ejecutor.

## Tensor-programa y procedencia 0.14

19. Un programa operativo completo contiene nueve tripletas: tres direcciones
    de entrada, tres direcciones de salida y la instrucción `(DO,DE,DS)`.
20. Las direcciones de celda son tripletas Aurora. El compilador solo traduce
    esas posiciones a referencias del autómata; no interpreta dominios,
    palabras, niveles ni acciones semánticas.
21. Una instrucción cerrada usa `DE=111`. Sus firmas homogéneas `000`, `111` y
    `222` representan respectivamente las direcciones aprender, inferir y
    deducir. Un `DE=222,DS=222` sigue siendo una instrucción indeterminada.
22. Tres programas candidatos compiten presentando sus nueve posiciones a
    nueve caras ordinarias. La síntesis conserva como hijos los tres candidatos
    de cada posición y debe reejecutarse completamente.
23. El programa emergente solo se ejecuta si sus seis direcciones son tripletas
    literales ordenables y su instrucción ha cerrado. Una dirección imposible
    conserva la hipótesis emergente, pero no activa el runtime.
24. La inducción tensorial no usa soporte entero, recencia, pesos, umbrales ni
    una elección externa de máximo.

25. Una semilla compilada conserva las nueve unidades educativas del programa,
    no solo sus valores decodificados. Todas deben reejecutarse.
26. Un disparo puede reflejarse como programa únicamente si esas nueve unidades
    coinciden exactamente con sus tres entradas, sus tres salidas y la
    instrucción realmente ejecutada.
27. Los candidatos nacidos de experiencia se agrupan solo cuando coinciden las
    huellas causales completas de sus tres señales progenitoras.
28. Cada tres experiencias consecutivas de la misma ventana se presentan a las
    nueve caras ordinarias de inducción. El runtime no vuelve a autorar sus
    programas ni les asigna una puntuación externa.
29. Las ventanas causales diferentes no compiten entre sí. Una ventana sin tres
    experiencias conserva su procedencia, pero no fabrica una síntesis.
30. La educación serializada conserva las unidades de procedencia y todos sus
    descendientes, de modo que el código aprendido no se aplana al reejecutarse.

## Diccionario fractal orientado por C-O 0.15 (prototipo histórico)

31. El diccionario operativo es un bosque ternario de programas, no una lista
    ordenada por una puntuación escalar.
32. Cada tres nodos del mismo nivel presentan sus nueve posiciones a nueve
    caras. El programa emergente ocupa automáticamente un nodo del nivel
    siguiente y conserva los tres programas inferiores como procedencia.
33. La posición `DO` del tensor-programa es también la unidad que ordena el
    nodo. No se añade metadato de prioridad.
34. En el prototipo 0.15, `C=0` recorre la rama de aprendizaje `0`; `C=1` recorre la rama de
    inferencia `1`; `C=2` mantiene la decisión abierta y delega el índice en la
    ordenación `O` de la unidad `DO`.
35. El trit de `DO` correspondiente a la rama elegida se convierte en la fase
    heredada por el nodo inferior. La misma regla se repite en cada escala.
36. Si `C=2` y la unidad `DO` no posee todavía una ordenación literal válida,
    ninguna rama es forzada y se conservan todos sus programas descendientes.
37. La orientación fractal no usa soporte, recencia, contadores, pesos,
    umbrales, máximos, `sort` ni una operación externa de reordenación.
38. Una raíz emergente cerrada se entrega directamente al mismo ejecutor
    relacional. Sus disparos pueden volver a reflejarse como código ordinario.

## Cara de salida lectora-escritora 0.16 (prototipo histórico)

39. Los tres tensores de salida consultan el mismo bosque en paralelo. La
    posición `0`, `1` o `2` de cada salida determina su dirección `C` de acceso.
40. Cada búsqueda devuelve un trit: `0` ausencia determinada, `1` coincidencia
    exacta reejecutable y `2` orientación todavía abierta.
41. Cualquier tripleta de hallazgos que contenga `2` permanece abierta. El
    sistema conserva las alternativas y no interpreta apertura como ausencia.
42. `111` reutiliza los tres tensores y permite continuar sin escribir.
43. `110`, `101` y `011` permiten cristalizar únicamente la posición cuyo
    estado es `0`. El tensor insertado es la salida ya producida, no un código
    construido por el diccionario, y debe ser ejecutable y reejecutable.
44. Tras la escritura, la posición ausente se relee desde su propio índice y
    debe producir `1`; la tripleta pasa a `111` antes de continuar.
45. Con cero o un hallazgo, la mayoría es `0`: el camino no escribe y devuelve
    los tres tensores de salida sin modificarlos.
46. Una búsqueda del bosque consulta niveles superiores antes que las fronteras
    causales nuevas. Esto permite releer una unidad recién escrita sin destruir
    ni reordenar una raíz anterior.

## Orientación fractal completa 0.17

47. `C` y `O` son dos momentos de la misma señal ternaria: `C` es la
    orientación recibida y `O` la orientación emitida. No se traducen mediante
    un segundo vocabulario de control.
48. En una tripleta ordenable, `O` determina la posición de `ES` y se cumple
    `ES=P[O]`. En el enlace vertical se cumple `ES↑=ES[O↑]`.
49. Toda SO y todo tensor-programa conservan una instrucción completa
    `K=(DO,DE,DS)`: la mayoría de `DS` expresa el `C` actual y `DO` conserva la
    orientación que puede presentarse a la relación siguiente.
50. Una presentación lee `DO[i]` como la siguiente orientación sin modificar
    ni reconstruir la unidad: `C[t+1]=DO[t][i]`. La regla propia de la escala
    determina `i`; en el diccionario, `C=2` delega ese índice en el orden local.
51. Una ventana abierta transporta `Carry(Unit(K,...))`, no un registro
    reducido `(DE,DO)`. Conserva `DO`, `DE`, `DS`, dirección, fotografía y los
    tres descendientes, y debe reejecutarse.
52. Los paquetes finales de `HDS`, `HDE` y `HDO` vuelven a proyectarse como un
    único `Kcontrol=(DOcontrol,DEcontrol,DScontrol)`.
53. Operación, coherencia y alcance son lecturas de los tres trits de
    `DScontrol`; el control completo puede reutilizarse como una `Unit`.
54. El perfil no asigna todavía por decreto un valor de orientación a ascenso,
    extensión o desplazamiento. Esos movimientos deberán emerger de conexiones
    tensoriales antes de retirar la orquestación experimental.

## Núcleo autosimilar 0.18.0-rc1

55. Toda relación canónica conserva una única `Unit(K)` con
`K=(DO,DE,DS)`. Carry, emergencia, información, conocimiento e instrucción no
son clases de objeto diferentes.
56. `C` selecciona una de las tres proyecciones de la misma unidad:
`K[0]=DO`, `K[1]=DE` y `K[2]=DS`. Una consulta por cualquiera de ellas devuelve
el `K` completo y su procedencia.
57. El diccionario almacena cada unidad una sola vez. Sus tres índices son tres
lecturas de su estructura, no tres copias ni tres memorias paralelas.
58. Una búsqueda sin coincidencias produce `0`; una coincidencia única y
reejecutable produce `1`; varias coincidencias compatibles producen `2` y
conservan todas las unidades completas.
59. Toda unidad presentada cumple `O=DO[C]` y `C[t+1]=O[t]`. Ningún valor de
orientación recibe una traducción intermedia.
60. Una topología contiene tres puertos indexados por `O`. El runtime entrega
el mismo objeto a las conexiones del puerto elegido y no interpreta sus
destinos como acciones semánticas.
61. Una conexión al nivel actual se observa como carry y una conexión al nivel
superior como emergencia. Estos nombres describen el recorrido; no alteran el
contenido, la identidad ni el tipo de `K`.
62. Una orientación abierta puede conservar simultáneamente conexiones del
nivel actual y del superior. El valor `2` no fuerza una tercera acción.
63. La ventana es la frontera final de una escala: sintetiza tres unidades,
lee `DO[C]` y presenta intacta la unidad resultante en el puerto seleccionado.
64. `DE` conserva conocimiento de cierre pero no selecciona por sí solo un
movimiento. Dos unidades con el mismo `DO` y distinto `DE` recorren la misma
conexión para un `C` común.
65. La promoción `1–3–9` aplica la misma cara, conserva los tres descendientes
y produce raíces consultables desde `DO`, `DE` y `DS`.
66. `fractal_kernel.py` no depende de clasificadores `ASCEND`, `CARRY`,
`SHIFT`, `CRYSTALLIZE`, `RETURN` o `OPEN`. Esas etiquetas permanecen únicamente
en prototipos históricos y pruebas de comportamiento.

## Estado de los prototipos 0.7–0.11

67. `growth.py` y `training.py` se conservan como oráculos experimentales.
    Demuestran cierre, extensión, recurrencia, competencia y selección
    contextual, pero programan explícitamente parte de esos comportamientos.
68. Sus resultados no se consideran ya semántica definitiva del runtime. Una
    conducta solo migrará al ejecutor universal cuando pueda expresarse con
    semillas, tensores, conexiones y reejecución.
69. El perfil 0.12 migró dos conductas: la realimentación abierta con los dos
    elementos siguientes y el crecimiento `9→3→1`. Ambas usan exactamente el
    mismo bucle relacional.
70. El perfil 0.13 migró la presentación completa a un tensor y probó la
    síntesis ternaria de programas competidores.
71. El perfil 0.14 hace que la experiencia causal refleje y presente esos
    programas sin una lista de candidatos escrita por el anfitrión. Derivar
    direcciones nunca observadas y realimentar continuamente el programa
    emergente permanecían como fronteras abiertas. El perfil 0.15 incorpora la
    promoción continua `3→1` y la navegación fractal mediante `C-O` dentro de
    una familia operativa. El perfil 0.16 incorpora la búsqueda paralela y la
    escritura conservadora de la única salida ausente. El perfil 0.17 convierte
    carry y control en unidades `K` completas y verifica el enlace `O→C` desde
    la tripleta hasta el control.

El release candidate no declara congelada una ruta Fibonacci ternaria, un
protocolo físico P2P ni una correspondencia automática entre cierre y
categorías lingüísticas humanas.
