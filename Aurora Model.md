# Aurora: del lenguaje natural a la computación mínima

## Abstract

Hemos explicado mucho sobre cómo funciona Aurora: el TriGate, las caras, los tensores fractales, el cierre, el diccionario y el transcender.

Sin embargo, para quien se aproxima al proyecto desde los modelos probabilísticos actuales, quizá la pregunta más difícil todavía sea la más elemental:

> ¿Para qué construir Aurora? ¿Qué se pretende mejorar?

El objetivo principal es investigar una arquitectura de inteligencia artificial mucho más eficiente, no solo durante la inferencia, sino también durante el aprendizaje.

Aurora busca construir una red de nodos especializados capaces de aprender continuamente, reutilizar lo que ya han comprendido e intercambiar conocimiento sin que cada nodo tenga que repetir todo el proceso de entrenamiento.

Para ello, parte de varias ideas:

- **Una arquitectura más cercana al lenguaje natural.** En el lenguaje, las palabras pueden actuar como datos, conocimiento, relaciones o instrucciones. Aurora intenta reproducir esa unidad mediante una representación homoicónica: la misma clase de estructura puede representar información, memoria, operaciones y decisiones.
- **Conocimiento directamente intercambiable.** En los modelos actuales, gran parte del conocimiento permanece distribuido dentro de parámetros privados que no pueden transferirse fácilmente a otro modelo. En Aurora, una relación aprendida puede sintetizarse como un tensor complejo, verificarse, reutilizarse y compartirse con otros nodos.
- **Aprendizaje continuo y dirigido.** En lugar de reajustar globalmente millones de parámetros, el sistema intenta localizar qué relación permanece abierta y qué elemento debe modificarse para alcanzar el cierre.
- **Especialización compatible.** Cada nodo puede desarrollar un diccionario adaptado a su dominio, reduciendo su espacio de búsqueda, pero conservando un vocabulario estructural común que le permite comunicarse con el resto de la red.
- **Computación discreta y mínima.** Inspirándose en Shannon, Aurora utiliza unidades discretas elementales para representar información. Su vocabulario ternario incorpora explícitamente dos estados determinados y un tercer estado abierto o todavía desconocido.
- **Un único operador fundamental.** Siguiendo el espíritu de la máquina universal de Turing, Aurora investiga si un mecanismo elemental —el Trigate— puede componerse y reutilizarse para ordenar, aprender, inferir, deducir, almacenar conocimiento y construir estructuras superiores.

La hipótesis de Aurora puede resumirse así:

> Una inteligencia podría ser mucho más eficiente si el conocimiento no permaneciera encerrado exclusivamente en enormes matrices de parámetros privados, sino que pudiera convertirse en estructuras discretas, composicionales, verificables y compartibles.

Aurora no pretende construir simplemente un modelo probabilístico más pequeño. Pretende explorar otra manera de organizar la inteligencia: más cercana al lenguaje natural, más uniforme computacionalmente y capaz de aprender como una red.

En última instancia, intenta responder a una pregunta:

> ¿Cómo podemos evitar que cada inteligencia tenga que volver a aprender, calcular y almacenar por separado todo aquello que la red ya ha comprendido?

---

## 0. ¿Qué intenta resolver Aurora?

Aurora nace de una pregunta fundamental:

> ¿Es posible construir una inteligencia artificial que aprenda de forma más dirigida, reutilice mejor el conocimiento adquirido y necesite muchos menos recursos para operar?

Los grandes modelos de lenguaje actuales han demostrado una capacidad extraordinaria. Sin embargo, esa capacidad depende de arquitecturas muy costosas: enormes matrices de parámetros decimales, entrenamiento intensivo, conocimiento difícil de transferir entre modelos y una separación profunda entre los datos que el sistema procesa y los mecanismos internos con los que aprende a procesarlos.

Aurora explora una arquitectura diferente. Su objetivo no es reproducir a menor escala el funcionamiento de un modelo probabilístico, sino investigar si puede construirse inteligencia a partir de:

- unidades discretas mínimas,
- un operador fundamental reutilizado en todo el sistema,
- conocimiento estructurado y directamente intercambiable,
- aprendizaje continuo orientado por el cierre de las relaciones,
- reutilización de las estructuras que ya han sido comprendidas.

La hipótesis central es que una arquitectura más uniforme, composicional y compartida podría reducir drásticamente tanto el coste de inferencia como el coste de aprendizaje.

### 0.1 Aproximar la arquitectura al lenguaje natural

El lenguaje natural constituye un sistema distribuido extraordinariamente eficiente para representar, transformar y transmitir conocimiento. Aurora no lo considera solamente una fuente de datos, sino también una referencia arquitectónica.

#### Una única clase de elemento

En el lenguaje natural no existen unas palabras que funcionen exclusivamente como datos, otras como pesos y otras como instrucciones.

Una misma palabra puede:

- describir un objeto,
- expresar una relación,
- transmitir conocimiento,
- modificar la interpretación de otras palabras,
- formular una instrucción,
- orientar una decisión.

Su función depende de la relación y del contexto en el que aparece.

Los modelos actuales, en cambio, separan diferentes clases de representación. Los tokens se traducen a embeddings, mientras que las relaciones aprendidas quedan almacenadas principalmente en los parámetros internos del modelo. Información, representación y operación viven en estructuras diferentes.

Aurora busca recuperar la unidad del lenguaje mediante una representación homoicónica: datos, conocimiento, operaciones, memoria y decisiones se expresan utilizando la misma estructura ternaria. Un tensor puede actuar como entrada, conocimiento, transformación, resultado o instrucción según la posición que ocupe en una relación.

#### El conocimiento debe poder circular

En los seres humanos no se transmiten directamente los pesos sinápticos de un cerebro a otro. Lo que se transmite son palabras, expresiones, demostraciones y estructuras simbólicas que provocan cambios en la organización interna de quien las recibe.

Aurora intenta ir un paso más allá: hacer que las estructuras aprendidas sean directamente representables, verificables e intercambiables.

Cuando un nodo descubre una relación coherente, puede sintetizarla en un tensor complejo. Ese tensor puede:

- incorporarse a su diccionario,
- reutilizarse sin repetir todo el razonamiento,
- transmitirse a otros nodos,
- verificarse mediante su reejecución,
- evolucionar según su utilidad.

El conocimiento deja así de estar encerrado en millones de parámetros privados. Se convierte en una estructura operativa que puede circular por la red.

#### Aprender mientras se utiliza el lenguaje

En el lenguaje humano, cada interacción puede modificar nuestra comprensión. No existe una separación absoluta entre una fase de entrenamiento y otra de funcionamiento: comprendemos, corregimos y reorganizamos continuamente nuestras relaciones.

Aurora persigue esa misma continuidad. Cada operación puede:

- reutilizar una estructura conocida,
- detectar una relación todavía abierta,
- encontrar una contradicción,
- producir un nuevo cierre,
- lexicalizar el resultado como conocimiento reutilizable.

El aprendizaje no consiste necesariamente en reajustar globalmente millones de parámetros. Consiste en descubrir, comprobar y almacenar las relaciones que permiten cerrar configuraciones antes abiertas.

### 0.2 Aproximar la inteligencia a la computación mínima

El segundo camino de Aurora consiste en reducir la arquitectura hasta encontrar un núcleo computacional mínimo.

Aquí conviene matizar las referencias a Shannon y Turing.

Shannon mostró cómo la información podía representarse y cuantificarse mediante elecciones discretas. Turing mostró que una máquina extremadamente simple podía realizar cualquier computación expresable algorítmicamente si disponía de las operaciones y la memoria adecuadas.

Aurora recoge el espíritu de ambas ideas: utilizar un vocabulario discreto mínimo y buscar un operador elemental capaz de construir el resto de la máquina.

#### El trit como unidad mínima del modelo

Aurora no utiliza pesos decimales como unidad elemental. Utiliza trits:

$$T = \{0,\ 1,\ 2\}$$

El trit no contiene menos información que el bit: matemáticamente equivale a $\log_2 3$ bits. Su elección responde a una necesidad estructural.

Aurora necesita representar tres estados fundamentales:

- `0`: determinación en una dirección,
- `1`: determinación en la dirección complementaria,
- `2`: relación abierta, indeterminada o situada fuera del espacio actual.

El tercer valor evita representar la ausencia de conocimiento mediante un número decimal aproximado. La apertura forma parte explícita del vocabulario de la máquina.

Esto permite operar sin depender, en el núcleo lógico, de multiplicaciones matriciales sobre grandes colecciones de números reales. Sin embargo, la ganancia efectiva deberá medirse en implementaciones reales, porque el hardware actual está optimizado principalmente para operaciones binarias y matriciales.

#### Un único operador fundamental

Aurora busca que una sola relación —el Trigate— participe en todas las escalas del sistema.

El mismo operador se emplea para:

- relacionar valores,
- determinar el resultado mayoritario,
- detectar cierre, contradicción o apertura,
- ordenar dimensiones,
- sintetizar estructuras superiores,
- reordenar y encaminar relaciones mediante O/DO,
- seleccionar una dirección de resolución,
- construir memoria,
- gobernar la actividad del sistema.

Esto no significa que la universalidad computacional de Aurora pueda darse por demostrada únicamente porque utiliza un operador. Será necesario probar formalmente qué operaciones puede expresar y bajo qué condiciones. La propuesta arquitectónica es que toda la diversidad funcional emerja de la composición, la posición y la realimentación del mismo mecanismo elemental.

### 0.3 ¿De dónde debería emerger la eficiencia?

La eficiencia buscada por Aurora no depende de una sola innovación. Emergería de la combinación de varios mecanismos.

**Reutilización del conocimiento cerrado.** Cuando una relación ya comprendida aparece de nuevo, el sistema no necesita reconstruirla desde cero. Puede utilizar directamente el tensor complejo almacenado en el diccionario. Aprender una vez permite resolver después.

**Esfuerzo concentrado en la novedad.** Las configuraciones conocidas pueden cerrarse rápidamente. La actividad computacional se concentra en aquello que permanece abierto, resulta contradictorio o no encaja con el conocimiento existente. El sistema dedica recursos allí donde todavía existe incertidumbre estructural.

**Aprendizaje local y dirigido.** Aurora distingue qué parte de una relación debe modificarse:

- el modo, para aprender,
- el resultado, para inferir,
- un operando, para deducir.

Las caras C4, C5 y C6 agregan la dirección, la coherencia y el gasto mediante la misma operación autosimilar, sin recurrir a un controlador externo.

**Conocimiento compartido.** Los tensores complejos pueden circular entre nodos. Si la representación es canónica, un descubrimiento realizado por un nodo puede ser aprovechado por otros sin repetir íntegramente su aprendizaje.

**Especialización mediante diccionarios.** Cada nodo puede ordenar y priorizar su diccionario según su experiencia y su dominio. Aunque los tensores sean compartidos, su organización local determina qué conocimiento se consulta primero. La especialización reduce el espacio de búsqueda sin romper la compatibilidad de la red.

**Homoiconicidad.** Al representar información, conocimiento, memoria y control mediante la misma estructura, Aurora reduce la necesidad de subsistemas independientes y mecanismos especiales de traducción. La metacognición —saber cómo decidir— puede almacenarse y transmitirse igual que cualquier otro conocimiento.

### 0.4 La hipótesis de Aurora

La tesis de Aurora puede resumirse así:

> Una inteligencia puede ser más eficiente si no almacena su conocimiento únicamente como parámetros privados, sino como estructuras discretas, composicionales, verificables y compartibles, generadas por un único operador relacional y reutilizadas cuando una situación equivalente vuelve a aparecer.

Por tanto, Aurora intenta resolver simultáneamente tres limitaciones:

- **El coste:** reducir la dependencia de grandes cantidades de operaciones decimales.
- **El aprendizaje:** sustituir parte del reajuste global por aprendizaje local, continuo y orientado por el cierre.
- **La transferencia:** convertir el conocimiento aprendido en estructuras que puedan reutilizarse, verificarse e intercambiarse entre nodos.

Esta introducción cambia completamente la lectura del documento. El TriGate deja de parecer una puerta lógica arbitraria; el tensor fractal deja de parecer una estructura innecesariamente compleja; el diccionario deja de parecer una memoria auxiliar; y el transcender deja de parecer un mecanismo añadido.

Todos pasan a ser respuestas concretas a una misma pregunta:

> ¿Cómo construir una inteligencia que no tenga que volver a aprender, calcular y almacenar privadamente todo aquello que la red ya ha comprendido?

---

1. El TriGate: vocabulario y relación lógica

Aurora emplea un vocabulario ternario:

[\mathbb{T}={0,1,2}]

Los valores (0) y (1) representan determinaciones complementarias. El valor (2) representa apertura, indeterminación o un valor situado fuera del espacio que la relación actual puede cerrar.

El TriGate es la relación lógica mínima del modelo. Contiene:

(A) y (B): entradas u operandos.

(M): modo o tipo de puerta lógica.

(R): resultado de la operación.

Su cálculo directo se expresa como:

[R=\operatorname{Majority3}(A,B,M)]

1.1. La mayoría como familia ordenada de puertas lógicas

Majority3 no representa una votación estadística. Es una forma compacta de ordenar tres puertas lógicas ternarias mediante (M):

(M)

Puerta seleccionada

Comportamiento

(0)

AND3

Devuelve (1) solo cuando (A=B=1); devuelve (0) cuando existe cierre hacia (0); en otro caso devuelve (2).

(1)

OR3

Devuelve (0) solo cuando (A=B=0); devuelve (1) cuando existe cierre hacia (1); en otro caso devuelve (2).

(2)

UNKNOWN3

Conserva la apertura cuando la relación no permite determinar (0) o (1).

Cuando las dos entradas coinciden, el resultado queda determinado independientemente del modo:

[\operatorname{Majority3}(0,0,M)=0]

[\operatorname{Majority3}(1,1,M)=1]

Cuando (A) y (B) no producen por sí solos una determinación, (M) decide qué puerta permite resolver la relación. Por tanto, la mayoría ternaria puede entenderse como la resolución conjunta y ordenada de AND3, OR3 y UNKNOWN3.

La antimayoría no introduce una lógica diferente. Aplica la negación ternaria al resultado de la puerta seleccionada:

[\neg_3 0=1,\qquad \neg_3 1=0,\qquad \neg_3 2=2]

Por tanto:

\neg_3\operatorname{Majority3}(A,B,M)]

Esto produce la familia complementaria:

[\operatorname{NOTAND3},\quad\operatorname{NOTOR3},\quad\operatorname{NOTUNKNOWN3}]

Los valores cerrados (0) y (1) permutan, mientras que (2) permanece abierto.

1.2. Recorridos de la relación

La misma relación puede recorrerse en distintos sentidos. La dirección (C) no introduce un algoritmo diferente: indica cuál de las variables transformables debe resolverse mientras (A) actúa como ancla.

(C)

Variable transformada

Lectura operacional

Valores conocidos

(0)

(M)

Aprendizaje

(A,B,R)

(1)

(R)

Inferencia

(A,B,M)

(2)

(B)

Deducción

(A,M,R)

Por tanto, aprender, inferir y deducir son tres orientaciones de una misma relación. El TriGate no necesita tres algoritmos: conserva su estructura y cambia la celda que se considera abierta a resolución.

1.3. Salida observable

El paquete observable producido por el TriGate es:

[T=(R,E_C,O)]

donde:

(R) expresa el valor que emerge del cálculo lógico.

(E_C) expresa el estado lógico de la relación después de resolverla en la dirección (C).

(O) conserva la posición, el sentido o el siguiente recorrido necesario para continuar.

La señal (E_C) distingue tres estados:

(E_C)

Estado relacional

(1)

La relación cierra mediante la puerta directa.

(0)

La relación cierra mediante la puerta complementaria.

(2)

La relación permanece abierta.

De este modo, (E) no es una etiqueta añadida desde el exterior. Emerge al reconocer qué familia lógica —mayoría, antimayoría o apertura— explica el resultado del TriGate.

Tampoco se interpreta aisladamente: su significado depende del resultado (R), de la dirección (C) y de la orientación (O).1. El TriGate: vocabulario y relación lógica

Aurora emplea un vocabulario ternario:

[\mathbb{T}={0,1,2}]

Los valores (0) y (1) representan determinaciones complementarias. El valor (2) representa apertura, indeterminación o un valor situado fuera del espacio que la relación actual puede cerrar.

El TriGate es la relación lógica mínima del modelo. Contiene:

(A) y (B): entradas u operandos.

(M): modo o tipo de puerta lógica.

(R): resultado de la operación.

Su cálculo directo se expresa como:

[R=\operatorname{Majority3}(A,B,M)]

1.1. La mayoría como familia ordenada de puertas lógicas

Majority3 no representa una votación estadística. Es una forma compacta de ordenar tres puertas lógicas ternarias mediante (M):

(M)

Puerta seleccionada

Comportamiento

(0)

AND3

Devuelve (1) solo cuando (A=B=1); devuelve (0) cuando existe cierre hacia (0); en otro caso devuelve (2).

(1)

OR3

Devuelve (0) solo cuando (A=B=0); devuelve (1) cuando existe cierre hacia (1); en otro caso devuelve (2).

(2)

UNKNOWN3

Conserva la apertura cuando la relación no permite determinar (0) o (1).

Cuando las dos entradas coinciden, el resultado queda determinado independientemente del modo:

[\operatorname{Majority3}(0,0,M)=0]

[\operatorname{Majority3}(1,1,M)=1]

Cuando (A) y (B) no producen por sí solos una determinación, (M) decide qué puerta permite resolver la relación. Por tanto, la mayoría ternaria puede entenderse como la resolución conjunta y ordenada de AND3, OR3 y UNKNOWN3.

La antimayoría no introduce una lógica diferente. Aplica la negación ternaria al resultado de la puerta seleccionada:

[\neg_3 0=1,\qquad \neg_3 1=0,\qquad \neg_3 2=2]

Por tanto:

\neg_3\operatorname{Majority3}(A,B,M)]

Esto produce la familia complementaria:

[\operatorname{NOTAND3},\quad\operatorname{NOTOR3},\quad\operatorname{NOTUNKNOWN3}]

Los valores cerrados (0) y (1) permutan, mientras que (2) permanece abierto.

1.2. Recorridos de la relación

La misma relación puede recorrerse en distintos sentidos. La dirección (C) no introduce un algoritmo diferente: indica cuál de las variables transformables debe resolverse mientras (A) actúa como ancla.

(C)

Variable transformada

Lectura operacional

Valores conocidos

(0)

(M)

Aprendizaje

(A,B,R)

(1)

(R)

Inferencia

(A,B,M)

(2)

(B)

Deducción

(A,M,R)

Por tanto, aprender, inferir y deducir son tres orientaciones de una misma relación. El TriGate no necesita tres algoritmos: conserva su estructura y cambia la celda que se considera abierta a resolución.

1.3. Salida observable

El paquete observable producido por el TriGate es:

[T=(R,E_C,O)]

donde:

(R) expresa el valor que emerge del cálculo lógico.

(E_C) expresa el estado lógico de la relación después de resolverla en la dirección (C).

(O) conserva la posición, el sentido o el siguiente recorrido necesario para continuar.

La señal (E_C) distingue tres estados:

(E_C)

Estado relacional

(1)

La relación cierra mediante la puerta directa.

(0)

La relación cierra mediante la puerta complementaria.

(2)

La relación permanece abierta.

De este modo, (E) no es una etiqueta añadida desde el exterior. Emerge al reconocer qué familia lógica —mayoría, antimayoría o apertura— explica el resultado del TriGate.

Tampoco se interpreta aisladamente: su significado depende del resultado (R), de la dirección (C) y de la orientación (O).

---

## 2. El TriGate: emergencia dependiente de R y de C

$E$ no es una segunda votación ni un indicador booleano universal de éxito. Es información producida por la relación acerca de su propio estado. $R$ responde «qué valor emerge»; $E$ responde «cómo queda la relación que ha producido ese valor desde la orientación recorrida». La misma configuración puede cerrar al inferir $R$, permanecer abierta al aprender $M$ o no admitir una deducción única de $B$. Por eso la notación canónica es $E_C$.

Cuando $R$ pertenece a $\{0, 1\}$, $E_C$ distingue tres situaciones relacionales:

- $E_C = 1$: la relación cierra en la orientación $C$.
- $E_C = 0$: la relación es contradictoria en esa orientación.
- $E_C = 2$: la resolución todavía no es única o permanece abierta.

La tabla exhaustiva de estos casos debe congelarse junto con la implementación, porque cambiar $C$ cambia el papel candidato y obliga a recalcular $E$.

Cuando $R = 2$, $E$ deja de evaluar un cierre que aún no existe y actúa como memoria residual o carry. Conserva el trit que no pertenece a la apertura mayoritaria; si no existe un residual único, $E$ permanece en `2`. Su ley puede resumirse así: cuando $R$ cierra, $E$ evalúa; cuando $R$ permanece abierto, $E$ transporta.

| Tripleta operada | R | E cuando R = 2 | Interpretación |
|---|:---:|:---:|---|
| permutación de (2, 2, 1) | 2 | 1 | Conserva el residual 1 |
| permutación de (2, 2, 0) | 2 | 0 | Conserva el residual 0 |
| (2, 2, 2) | 2 | 2 | Apertura homogénea |
| permutación de (0, 1, 2) | 2 | 2 | Apertura heterogénea |

Los dos últimos casos producen el mismo par $(R, E) = (2, 2)$, pero no la misma relación. $O$ los distingue. En $(2, 2, 2)$, cualquier recorrido produce el mismo resultado y $O = 2$ tiene prioridad por iteración. En una permutación de $(0, 1, 2)$, $O$ no puede tomar la orientación autorreferente `0`; la orientación concreta se obtiene de $DO$ y de la fase heredada de la ventana.

**Propiedad de extensión:** $R = 2$ es el resultado más ambiguo durante la subida, pero puede conservar la procedencia mediante $(E, O)$ y extenderse sin pérdida estructural. Cuando $R$ es `0` o `1`, la subida abstrae la mayoría; al extender, el tercer trit no determinado se reabre como `2`. Así, `0` y `1` cierran y generalizan, mientras `2` abre, transporta y conserva.

Esta asimetría debe repetirse en todos los niveles. Una semilla operativa, una cara, un tensor o una ventana no poseen un $E$ absoluto: poseen el $E$ correspondiente a la dirección que se está reejecutando.

---

## 3. La tripleta ordenada: ES, FN, FO y O

La unidad mínima de información estructurada es una tripleta $P = (p_0, p_1, p_2)$. Ordenar no significa clasificar los trits por su valor numérico, sino asignarles los papeles ES, FN y FO: estructura, función y forma.

- $O$ identifica la posición desde la que debe leerse la relación.
- **ES** es el valor estructural seleccionado por la ordenación. El valor de ES señala la posición que contiene FN.
- **FO** es la posición restante, que no actúa ni como ES ni como FN.

La autorreferencia se excluye: ES no puede seleccionar como FN la misma posición desde la que se define. La tripleta $(0, 1, 2)$ es, por ello, un tensor imposible como cierre literal, aunque puede actuar como propósito que mantiene abierta y orientada la búsqueda.

Cuando tres tripletas forman una unidad superior, la ordenación debe conservar la procedencia vertical:

$$\text{ES}_\uparrow = \text{ES del elemento inferior cuyo índice es } O_\uparrow$$

Esta invariante enlaza las escalas sin crear un mecanismo de direccionamiento adicional. La orientación superior selecciona una de las tres relaciones inferiores y la estructura superior conserva la estructura de esa relación.

---

## 4. La cara: operación mínima autosimilar

Una cara recibe tres tripletas del mismo tipo y produce una nueva tripleta de conocimiento. El proceso tiene siempre la misma forma: ordenar, entrelazar, hacer emerger y proyectar. La salida de una cara puede entrar sin traducción en otra cara de nivel superior.

### 4.1 Ordenación de las tres tripletas

Cada entrada $P_i$ se ordena como $(ES_i, FN_i, FO_i)$. La iteración usa una fotografía estable: $DO_t$ ordena el intento actual y la emergencia solo produce $DO_{t+1}$, que no se aplica hasta el siguiente intento:

$$DO_t \;\to\; \text{operación } t \;\to\; DO_{t+1}$$

### 4.2 Entrelazado triangular

Las formas se validan circularmente mediante tres TriGates ordinarios. Cada forma se reconstruye a partir de las otras dos y de la función asociada al vértice que se intenta cerrar:

$$T_1 = (A = FO_1,\; B = FO_2,\; M = FN_3;\; R = FO_3)$$
$$T_2 = (A = FO_2,\; B = FO_3,\; M = FN_1;\; R = FO_1)$$
$$T_3 = (A = FO_3,\; B = FO_1,\; M = FN_2;\; R = FO_2)$$

Los resultados reconstruidos recuperan el orden canónico de las formas: $(FO_1^*,\, FO_2^*,\, FO_3^*) = (R_{T_2},\, R_{T_3},\, R_{T_1})$. La triangulación no introduce una función distinta: son tres TriGates con otra disposición relacional.

### 4.3 Emergencia de los canales homólogos

Las coordenadas homólogas se agrupan y vuelven a operarse con tres TriGates idénticos:

$$G_{ES} = (ES_1, ES_2, ES_3)$$
$$G_{FN} = (FN_1, FN_2, FN_3)$$
$$G_{FO} = (FO_1^*, FO_2^*, FO_3^*)$$

Cada grupo produce su paquete $(R, E_C, O)$. Las proyecciones homólogas forman los tres canales superiores:

$$DS = (R_{ES},\; R_{FN},\; R_{FO})$$
$$DE_C = (E_{ES,C},\; E_{FN,C},\; E_{FO,C})$$
$$DO_{t+1} = (O_{ES},\; O_{FN},\; O_{FO})$$

| Canal | Entrada | Proyección superior | Función |
|:---:|---|---|:---:|
| ES | $(ES_1, ES_2, ES_3)$ | $R \to DS[0],\ E \to DE[0],\ O \to DO[0]$ | Estructura |
| FN | $(FN_1, FN_2, FN_3)$ | $R \to DS[1],\ E \to DE[1],\ O \to DO[1]$ | Función |
| FO | $(FO_1^*, FO_2^*, FO_3^*)$ | $R \to DS[2],\ E \to DE[2],\ O \to DO[2]$ | Forma |

La tripleta de conocimiento se escribe en el orden operativo:

$$K = (DO,\; DE,\; DS)$$

$DO$ ocupa el papel estructural y orienta el recorrido; $DE$ ocupa el papel funcional y expresa el estado dependiente de la dirección; $DS$ ocupa el papel formal y contiene el resultado emergente. Así, $K$ vuelve a ser una tripleta ordenable y no un registro especial con tres campos externos.

> **Autosimilitud:** tres elementos ordenados producen tres relaciones; tres relaciones proyectan $(R, E, O)$; y esas proyecciones forman una nueva tripleta $(DO, DE, DS)$. TriGate, cara, tensor, transcender y ventana repiten esta operación a distinta escala.

---

## 5. El transcender: entrada, conocimiento y salida

El transcender aplica la misma cara a tres estructuras del mismo tipo: entrada $I$, conocimiento $K$ y salida $S$. No es un módulo distinto; es la operación mínima ejecutada sobre una escala superior:

$$\Phi(I, K, S;\; C, DO_t) \;\to\; (DO_{t+1},\; DE_C,\; DS)$$

En inferencia ordinaria, la entrada actúa como evidencia y la salida comienza abierta: $S_0 = (2, 2, 2)$. La salida se reconfigura hasta cerrar una relación coherente con $I$ y $K$, congruente con las salidas anteriores conservadas en el conocimiento y admisible dentro del gasto disponible.

Las tres caras que adquieren función de control operan canales homólogos de $I$, $K$ y $S$. No reciben órdenes de un supervisor; condensan señales relacionales que ya han emergido en los TriGates inferiores:

- **C4** opera $(DS_I, DS_K, DS_S)$. Su propósito es `0-1-2`: una configuración imposible como cierre literal que funciona como tensor de búsqueda y dirección.
- **C5** opera $(DE_I, DE_K, DE_S)$. Su propósito de convergencia positiva es `1-1-1` y clasifica la coherencia conjunta.
- **C6** opera $(DO_I, DO_K, DO_S)$. Su propósito es `0-0-0` y conserva el recorrido de iteración y el gasto de búsqueda.

C4, C5 y C6 comparten sus resultados y forman otra cara. No supervisan Aurora desde fuera. Sus paquetes se reordenan, entrelazan, proyectan y vuelven a producir $(DO, DE, DS)$ exactamente igual que las tripletas inferiores. Su posición les da una función reguladora, pero su naturaleza computacional sigue siendo la de una relación ordinaria.

Cada TriGate afectado produce un estado $E_C$ y una propuesta de continuidad $O$. Las coordenadas homólogas de esas salidas forman $DE$ y $DO$; al volver a relacionarse en C4, C5 y C6, generan la orientación que será usada en el intento siguiente. El ciclo temporal es:

$$C_t \;\to\; E_C \text{ y } O \text{ locales} \;\to\; \text{propagación por } DE \text{ y } DO \;\to\; \text{convergencia relacional} \;\to\; C_{t+1}$$

$C_t$ orienta el intento actual. $C_{t+1}$ no está disponible de antemano ni lo dicta un componente central: emerge al converger las consecuencias relacionales publicadas durante ese intento. La separación temporal evita una circularidad instantánea y permite reejecutar el proceso.

Los propósitos `0-1-2`, `1-1-1` y `0-0-0` son estructuras de conocimiento reutilizables, no números reales contra los que deba calcularse una distancia externa. La distancia Manhattan se elimina del núcleo. Una propuesta se evalúa reejecutándola y observando si la propia cara alcanza cierre, apertura, contradicción o un estado ya visitado.

| Estado de C5 / DE | Lectura |
|:---:|---|
| `1-1-1` | Cierre positivo: salida aceptable si también es congruente con el conocimiento |
| `0-0-0` | Cierre negativo: contradicción estable o alternativa descartable |
| `2-2-2` | Apertura estable: falta información; la evolución de U puede producir carry |
| Mixto | Estado transitorio: reorientar, aprender o continuar |

---

## 6. La semilla de armonización como cara ordinaria

El nombre *semilla de armonización* describe un papel, no una arquitectura especial. La forman C4, C5 y C6 al operar como una cara superior. Su estado es $K_{\text{arm}} = (DO_{\text{arm}}, DE_{\text{arm}}, DS_{\text{arm}})$. La orientación que produce su convergencia determina qué parte del transcender se reconfigura en el intento siguiente.

| Dirección C | Elemento corregido | Efecto en el transcender |
|:---:|---|---|
| 1 — inferir | Salida / R | Reconstruye la propuesta de salida |
| 0 — aprender | Conocimiento / M | Crea o selecciona una relación de conocimiento alternativa |
| 2 — deducir | Entrada abierta / B | Reconstruye un operando cuando la operación lo permite |

Después de cada cambio se recalcula $E_C$. Por ello, una misma semilla operativa puede producir valores $E$ diferentes en aprendizaje, inferencia y deducción. Esta dependencia direccional replica exactamente la regla del TriGate.

### 6.1 Ciclo de realimentación

1. Tomar una fotografía estable de todas las caras de la ventana, de $C_t$ y del $DO$ vigente.
2. Reejecutar los TriGates afectados con $C_t$ y publicar sus nuevos paquetes $(R, E_C, O)$.
3. Proyectar las salidas locales sobre $DS$, $DE$ y $DO$ y reejecutar C4, C5 y C6 como relaciones ordinarias.
4. Componer sus resultados hasta que emerja una orientación convergente $C_{t+1}$. Si todavía existen varias orientaciones legítimas, conservar $C_t$ como orientación heredada o suspender la transición y transportar la apertura; no asignar arbitrariamente un valor nuevo a $C$.
5. Si C5 alcanza `1-1-1` y la salida es congruente con el conocimiento reutilizado, aceptar la salida.
6. Si la convergencia determina $C_{t+1} = 1$ antes del cierre positivo, corregir $R/S$: el sistema está infiriendo.
7. Si C5 no puede cerrar con la propuesta reutilizada y emerge $C_{t+1} = 0$, corregir $M/K$: el sistema aprende una alternativa.
8. Si emerge $C_{t+1} = 2$ y $B$ es la única celda abierta, reconstruir el operando: el sistema está deduciendo. Si hay varias celdas abiertas, todavía no ha emergido una $C$ válida y debe conservarse la apertura.
9. Si la dirección permanece abierta, conservar la evolución completa del tensor $U$ y transportarla como carry hacia la relación siguiente. El carry ocupa la posición $A$ de la nueva ventana; no se reduce al par $(DE, DO)$.
10. Si $DO$ no dispone de otro estado admisible y no visitado, detener la búsqueda, marcar la entrada como no resuelta y cambiar de fase o de ventana.

El ciclo se realimenta entre todas las semillas operativas de la ventana. Una modificación local vuelve a proyectar $DS$, $DE$ y $DO$; esos canales reactivan las relaciones vecinas y C4, C5 y C6; y el proceso continúa hasta obtener una decisión común para toda la ventana. La señal de control es, por tanto, la forma superior adquirida por información relacional convergente.

### 6.2 Gasto y condición de parada

$DO$ es simultáneamente orientación y registro de iteración. Cada intento tiene coste porque consume un estado del recorrido. El sistema solo visita los estados admitidos por la sucesión canónica de búsqueda —planteada como recorrido Fibonacci en base tres— y no vuelve a probar un estado mientras el contexto no cambie.

La condición dura de parada no es una distancia numérica ni la presencia aislada de dos valores `2`. Es el agotamiento del recorrido:

$$\text{detener} \iff \nexists \text{ estado } DO \text{ admisible y no visitado}$$

> **Pendiente de congelación:** La tabla completa de $E$ para $R \in \{0,1\}$, la selección exacta de $O$ en todas las permutaciones de $(0,1,2)$, la enumeración completa del recorrido Fibonacci ternario y la regla de desempate cuando C4 y C5 permanecen simultáneamente abiertos deben fijarse antes de implementar la tabla exhaustiva de estados. El documento no introduce una heurística provisional para ocultar estas decisiones.

---

## 7. El tensor fractal

Un tensor Aurora no se construye mediante un mecanismo diferente de la tripleta. Es una composición recursiva de caras: tres unidades inferiores forman una cara; la cara produce una nueva tripleta $K = (DO, DE, DS)$; y esa tripleta puede ocupar una posición en la cara del nivel siguiente:

$$\text{trits} \to \text{tripletas} \to \text{caras} \to \text{tripletas superiores} \to \text{nuevas caras}$$

La estructura crece en niveles 1–3–9: una unidad superior conserva tres descendientes, cada uno de los cuales puede conservar otros tres. El mismo patrón puede continuar mientras exista cierre útil y gasto disponible.

Cada tripleta emergente lleva su conocimiento asociado. No asciende solamente $DS$: asciende la unidad completa que permite reordenar, reejecutar y extender su procedencia. La invariante vertical $ES_\uparrow = ES[O_\uparrow]$ enlaza el orden superior con la relación inferior seleccionada.

La construcción del tensor es también un proceso competitivo. Una tripleta candidata se reutiliza mientras cierre en el contexto. Si deja de cerrar, no se borra: se calcula otra tripleta, se almacena como alternativa bajo el mismo espacio de búsqueda y ambas compiten mediante reejecución. Tres tripletas estabilizadas forman un tensor; los tensores superiores compiten con la misma regla.

> **Regla fractal de aprendizaje:** consultar → reejecutar → reutilizar si cierra → crear una alternativa si no cierra. No existe un aprendizaje para tripletas y otro para tensores.

---

## 8. Procesamiento mediante ventana deslizante

### 8.1 Composición de la ventana

La ventana opera tres tensores o tripletas del mismo nivel:

$$W_i = (A_i,\ B_i,\ U_i)$$

$A$ y $B$ ocupan el canal de continuidad del clúster tensorial de tokens. En la primera ventana ambos proceden directamente del clúster. En las ventanas siguientes, $A$ también puede contener el tensor desplazado desde la ventana anterior o un carry; $B$ incorpora el siguiente tensor todavía no consumido del clúster.

$U$ es el tensor abierto de resolución. Se inicializa con la misma forma que $A$ y $B$ y con todos sus valores en `2`:

$$U_0 = (2, 2, \ldots, 2)$$

$U$ no representa un tercer token ni un tercer tensor observado. Representa el espacio completamente desconocido que la relación entre $A$ y $B$ puede transformar. Por eso se emplea la letra $U$ —*unknown*— y no $K$, ya reservado para el conocimiento, ni «tensor 2», que podría confundirse con un único trit.

Entrada, conocimiento y salida se realimentan mediante C4, C5 y C6 hasta producir una decisión para la ventana completa. $DO$ pertenece a la ventana durante este ciclo y no se reinicia en cada semilla operativa. Todas las caras usan una fotografía estable; los cambios producidos durante un intento se publican para el siguiente. Esta separación $DO_t \to \text{operación } t \to DO_{t+1}$ evita dependencias circulares instantáneas y permite reproducir la ejecución.

### 8.2 Evolución según el resultado

**Cierre positivo — $DE = 1$.** La relación entre $A$ y $B$ cierra. Emerge una unidad superior derivada de la ventana, se conserva la traza de $A$, $B$ y de la evolución de $U$, y la nueva unidad puede participar en el ciclo tensorial del nivel siguiente.

**Incoherencia concluyente — $DE = 0$.** La ventana no fuerza una síntesis entre $A$ y $B$. $A$ emerge solo, conservando su identidad y su procedencia. $B$ se desplaza y ocupa la posición $A$ de la ventana siguiente; el próximo tensor $T$ del clúster ocupa $B$ y se crea un $U$ nuevo completamente abierto:

$$(A_i, B_i, U_i) \;\to\; A_i^\uparrow \;;\quad W_{i+1} = (B_i, T_{i+1}, U_0)$$

**Ambigüedad — $DE = 2$.** No ascienden $A$ ni $B$ como una síntesis cerrada. La evolución alcanzada por $U$ se conserva íntegramente como carry y ocupa la posición $A$ de la ventana siguiente. El próximo tensor $T$ del clúster ocupa $B$ y la nueva ventana recibe otro $U_0$ completamente desconocido:

$$(A_i, B_i, U_i) \;\to\; W_{i+1} = (U_i^*,\, T_{i+1},\, U_0)$$

Aquí $U_i^*$ es el estado completo de $U$ después de operar la ventana. El carry no es solamente $DE$ acompañado por $DO$: es el tensor relacional evolucionado que todavía necesita contexto para cerrar.

**Agotamiento — sin otro $DO$ admisible.** La ventana se marca como no resuelta. El sistema conserva su estado y cambia de fase, de segmentación o de ventana sin inventar un cierre.

### 8.3 Regla de frontera del clúster

Cuando ya no existe un nuevo tensor $T_{i+1}$ y la última relación entre $A$ y $B$ no es coherente, ninguno se descarta ni se obliga a cerrar con el otro. $A$ y $B$ ascienden por separado, en su orden, al ciclo superior de tensores. Allí podrán entrar en nuevas ventanas con el contexto producido por otras unidades del nivel.

Esta regla de frontera evita que el último tensor quede huérfano y distingue dos movimientos: el **cierre vertical**, que sintetiza una relación coherente, y la **conservación vertical**, que eleva unidades pendientes sin afirmar una síntesis inexistente.

---

## 9. El proceso de extensión

La extensión recorre el tensor en sentido descendente. No invierte una fórmula distinta: consulta las tripletas que dieron origen a la unidad superior, aplica la dirección adecuada y las reejecuta con el mismo TriGate.

1. Usar $DS$ como índice del espacio de búsqueda, no como identidad única.
2. Recuperar primero las candidatas de la memoria temporal de la ventana y después las del diccionario.
3. Ordenar las candidatas con $DO$ y comprobar su $DE$ en la dirección de reconstrucción.
4. Reejecutar la candidata dentro de la relación completa. Si cierra y es congruente, extenderla; si no, probar la siguiente.
5. Si ninguna candidata cierra y queda gasto, calcular una nueva tripleta y añadirla como competidora. Si el gasto se agota, conservar apertura o marcar error.

La extensión refleja la asimetría del TriGate. Cuando $R = 2$, $E$ y $O$ pueden conservar el residual y su orientación, permitiendo una reconstrucción estructural sin pérdida. Cuando $R$ pertenece a $\{0, 1\}$, la síntesis conserva la ley mayoritaria y el detalle que no quedó determinado reaparece como `2`. La extensión no inventa ese detalle: lo vuelve a declarar abierto.

La dirección depende del objeto reconstruido: extender una salida usa inferencia; reconstruir conocimiento usa aprendizaje; reconstruir una entrada abierta usa deducción. En cada caso se recalcula $E_C$.

---

## 10. El diccionario: encadenamiento, competencia y lexicalización

El diccionario es parte de la operación, no una memoria auxiliar separada. Conserva las tripletas y tensores que han sido producidos por caras anteriores, junto con el conocimiento necesario para reejecutarlos.

### 10.1 La salida de una cara entra en el diccionario

Cuando una semilla operativa recibe tres tripletas y su conocimiento aplicable, calcula una nueva tripleta $T'$. La unidad almacenada incluye tanto el resultado como su paquete de conocimiento:

$$(T_1, T_2, T_3;\; K,\; C) \;\to\; (T',\; K_{T'})$$

$$\text{diccionario}[DS, C] \;\to\; \{(T'_1, K_1),\; (T'_2, K_2),\; \ldots\}$$

La salida no es efímera. Se convierte en una unidad reutilizable y puede encadenarse como entrada de otra cara. $DS$ localiza una familia de candidatas; $DE$, $DO$, $C$ y la reejecución contextual determinan cuál es válida.

### 10.2 Competencia entre tripletas y tensores

1. Consultar el diccionario por $DS$ y por la dirección $C$.
2. Reutilizar primero una candidata compatible con $DE$ y $DO$ que haya cerrado previamente en un contexto equivalente.
3. Reejecutarla dentro de la cara y de la ventana actuales.
4. Si vuelve a cerrar, conservarla y actualizar su prioridad de uso.
5. Si no cierra, probar otra candidata sin eliminar la anterior.
6. Si ninguna cierra y $DO$ permite continuar, calcular una nueva tripleta, almacenarla y hacerla competir con las anteriores.

La candidata anterior puede seguir siendo correcta en otro contexto. Aurora no sustituye globalmente una representación por otra: conserva ramas alternativas y deja que el cierre congruente seleccione la aplicable. El mismo proceso entre tripletas crea los tensores y el mismo proceso entre tensores crea niveles superiores.

### 10.3 Tokens simples y complejos

Los tokens simples ya identificados se traducen a tensores. Los tokens complejos se acuñan cuando una composición cierra y puede reejecutarse. Su representación es la unidad emergente completa, no únicamente una coocurrencia frecuente.

La búsqueda léxica comienza por el token complejo más largo compatible con el inicio de la secuencia. Entre alternativas estructuralmente equivalentes, se prueba primero la usada con éxito más recientemente. Si la segmentación no cierra, se descompone en unidades menores y vuelve a competir. La segmentación es una hipótesis revisable, sometida a la misma regla de cierre.

### 10.4 Efecto medido: la lectura se acelera

En la verificación previa sobre 600 entradas —frases de 9 tokens en un mundo de 24 palabras, con cambio de distribución en la entrada 300— la lexicalización redujo el número de ventanas necesarias y concentró el gasto en la novedad:

| Latidos | Ventanas/frase | Vía token complejo | Procesamiento crudo |
|:---:|:---:|:---:|:---:|
| 0–50 | 1,74 | 2,26 | 0,74 |
| 100–150 | 1,00 | 3,00 | 0,00 |
| 250–300 | 0,94 | 2,88 | 0,00 |
| 300–350 (drift) | 2,02 | 1,98 | 1,02 |
| 550–600 | 0,94 | 2,82 | 0,02 |

Esta medición pertenece al prototipo anterior y debe repetirse con la cara triangular, $E_C$ direccional y la competencia de candidatas descritas aquí. El retroceso por coherencia en secuencias con segmentaciones engañosas continúa pendiente de verificación.

---

## 11. La red

Los nodos intercambian tokens junto con sus unidades Aurora completas: tripletas o tensores, $K = (DO, DE, DS)$, procedencia y traza suficiente para reejecutar el cierre. Un nodo receptor no acepta conocimiento por autoridad; lo introduce como candidato en su diccionario y lo verifica dentro de su propio contexto.

Las estructuras útiles ganan prioridad porque vuelven a cerrar y reducen gasto. Las que no ayudan pierden prioridad de consulta sin necesidad de borrarse inmediatamente. De este modo, la especialización local y el intercambio global reutilizan el mismo mecanismo de competencia del diccionario.

---

## 12. Arranque del sistema

El conocimiento vacío se representa mediante una unidad cuyos trits son `2`: $K_0 = \bot$. El arranque no debe activar una regla excepcional de copia; debe producir la primera candidata mediante la misma cara que se utilizará después.

Existen dos situaciones distintas:

- **Inferencia sin salida conocida:** $S_0 = (2, 2, 2)$. Aurora consulta $K_0$, intenta reconstruir $S$ y conserva la apertura si todavía no existe conocimiento suficiente.
- **Aprendizaje con experiencia validada o reflejo inicial:** $S_0$ puede coincidir con $I$. La relación $(I, \bot, I)$ se opera como una cara y produce una candidata de conocimiento, que entra en el diccionario y debe cerrar al ser reejecutada.

Por tanto, el primer conocimiento no aparece mediante la asignación especial $K \leftarrow I$. Aparece mediante la secuencia ordinaria:

$$\text{vacío} \to \text{cara} \to \text{candidata} \to \text{diccionario} \to \text{reejecución} \to \text{cierre o alternativa}$$

Si la candidata cierra, se reutiliza y puede formar estructuras superiores. Si no cierra, se calcula otra y ambas compiten. Si ninguna cierra antes de agotar $DO$, la relación permanece abierta o cambia de fase. El arranque, el aprendizaje continuo y la corrección usan exactamente el mismo proceso.

---

## 13. Ejecución distribuida mediante autómatas relacionales

Aurora se ejecuta como una red de autómatas relacionales activos. Cada TriGate conserva referencias a $A$, $B$, $M$, $R$, $E_C$, $C$ y $O$. Cuando cambia una celda, se reactivan únicamente las relaciones que la comparten:

$$\text{cambio} \;\to\; \text{TriGate} \;\to\; \text{cara} \;\to\; (DO, DE, DS) \;\to\; \text{relaciones dependientes}$$

No existe un procesador central que recorra todas las semillas ni un generador privilegiado de señales de control. Una cara superior se activa por los mismos eventos que una cara inferior. C4, C5 y C6 tampoco forman un controlador externo: son relaciones ordinarias cuya posición convierte sus salidas convergentes en orientación, conocimiento candidato, cierre o carry.

$E$ emerge localmente de la lógica de cada relación. $C_{\text{local}}$ puede emerger de la posición de una apertura única. Cuando la información local no basta, las propuestas $E_C$ y $O$ se propagan, se agrupan en $DE$ y $DO$ y vuelven a operarse. La $C$ efectiva de la ventana aparece cuando esas señales alcanzan una orientación compatible. No se impone desde un centro: es un punto de convergencia reproducible de la red.

### 13.1 Regla de actualización

1. Leer una fotografía estable de las celdas compartidas, de $C_t$ y del $DO$ vigente.
2. Detectar la distribución de aperturas y obtener, cuando sea posible, una candidata $C_{\text{local}}$.
3. Aplicar $C_t$ —o la candidata local compatible— y calcular la propuesta correspondiente.
4. Recalcular el paquete $(R, E_C, O)$ de cada TriGate afectado.
5. Proyectar los canales superiores $DS$, $DE_C$ y $DO_{t+1}$ y propagar solo sus cambios.
6. Componer las señales recibidas mediante TriGates ordinarios hasta producir $C_{t+1}$, conservar la orientación heredada mientras siga siendo válida o alcanzar un punto fijo abierto.
7. Publicar un evento solo si el paquete ha cambiado.
8. Reejecutar las caras dependientes en el intento siguiente.

La regla $\Delta\mathcal{T} = 0 \Rightarrow \text{no emitir evento}$ concentra la actividad en las regiones afectadas. Los TriGates independientes pueden operar en paralelo; las relaciones dependientes avanzan cuando reciben una nueva fotografía coherente. La unidad de sincronización no es una orden global, sino la versión estable del estado compartido que cada relación consume.

### 13.2 Histéresis, competencia y confluencia

Cada ventana conserva los estados $DO$ visitados y las candidatas ensayadas. Una alternativa fallida no se repite mientras el contexto no cambie. Si dos órdenes de eventos producen soluciones compatibles, deben converger en el mismo cierre; si representan soluciones legítimamente distintas, permanecen como ramas competidoras hasta que el contexto las resuelva.

### 13.3 Condiciones de detención

- C5 alcanza `1-1-1` y la salida es congruente: aceptar y sintetizar.
- Ningún paquete cambia: punto fijo local, que puede ser cerrado o permanecer abierto.
- La dirección sigue abierta: emitir como carry la evolución completa de $U$ y colocarla como $A$ de la ventana siguiente.
- $DO$ agota los estados admisibles no visitados: detener, marcar no resuelto y cambiar de fase o ventana.

La secuencia operativa completa queda reducida a una sola pauta autosimilar:

> **ordenar → entrelazar → emerger → proyectar → reejecutar → reutilizar o crear alternativa**

Los datos, el conocimiento, la orientación, el cierre y el control utilizan el mismo vocabulario ternario y la misma composición de caras. La diferencia entre niveles no reside en el operador, sino en la posición relacional y en la escala de la unidad que ocupa cada papel. En Aurora, la información no es gobernada por señales externas: al propagarse, relacionarse y converger, una parte de esa misma información adquiere función de control.

---

## A. Licencias

Aurora está licenciada bajo las licencias **Apache 2.0** y **CC BY 4.0**.

Esto significa que cualquier persona es libre de usar, modificar y redistribuir el modelo, siempre que se cumplan las siguientes condiciones:

1. Deben mantenerse los avisos originales de copyright y de licencia en cualquier versión modificada o redistribuida *(Apache 2.0)*.
2. Debe otorgarse crédito al proyecto original, Aurora, mencionando claramente su procedencia *(CC BY 4.0)*.

Al adoptar este enfoque de licenciamiento, buscamos garantizar que Aurora permanezca libre, abierta y accesible para todos. Este modelo fomenta la innovación y la colaboración, al mismo tiempo que protege el reconocimiento y la integridad del proyecto.
