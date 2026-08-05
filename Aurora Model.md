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

El diccionario local y la red distribuida no requieren dos algoritmos de búsqueda. En ambos casos, buscar consiste en reconstruir por deducción el elemento que completa una relación. La única diferencia es la escala: localmente se deduce un tensor de conocimiento; en la red se deduce el tensor-identidad del nodo capaz de ayudar.

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

## 1. El TriGate: vocabulario y relación lógica

Aurora emplea un vocabulario ternario $T = \{0, 1, 2\}$. Los valores `0` y `1` representan determinaciones complementarias; `2` representa apertura, indeterminación o un valor situado fuera del espacio que la relación actual puede cerrar.

El TriGate es la relación mínima del modelo. Contiene dos operandos $A$ y $B$, un modo lógico $M$ y una celda de resultado $R$. La operación ordinaria calcula una propuesta de resultado mediante la mayoría ternaria:

$$\hat{R} = \text{Majority}_3(A, B, M)$$

La misma relación puede recorrerse en sentido inverso. La dirección $C$ no introduce otra operación: indica cuál de las tres variables transformables debe resolverse mientras $A$ actúa como ancla.

- **C = 0:** reconstruir $M$ a partir de $A$, $B$ y $R$; aprendizaje.
- **C = 1:** reconstruir $R$ a partir de $A$, $B$ y $M$; inferencia.
- **C = 2:** reconstruir $B$ a partir de $A$, $M$ y $R$; deducción o búsqueda.

La deducción se expresa mediante el dominio compatible:

$$D(A, M, R) = \{B \in \{0,1,2\} \mid \text{Majority}_3(A, B, M) = R\}$$

El dominio puede ser vacío, contener una solución única o conservar varias candidatas. Un trit `2` es un valor literal posible; no debe confundirse con un conjunto de varias soluciones. La multiplicidad pertenece al dominio de candidatas y a su estado $E_C$.

Por tanto, inferir, deducir y aprender son tres orientaciones de una misma relación. El TriGate no necesita tres algoritmos: conserva una estructura y cambia la celda que se considera abierta a corrección.

El paquete observable del TriGate es:

$$\mathcal{T} = (R,\ E_C,\ O)$$

$R$ expresa el valor emergente; $E_C$ expresa el estado emergente después de resolver en la dirección $C$; $O$ conserva la posición, el sentido o el siguiente recorrido necesario para continuar. $E$ no se interpreta de forma aislada: depende de $R$, de $C$ y de $O$.

---

## 2. El TriGate: emergencia dependiente de R y de C

$E$ no es una segunda votación ni un indicador booleano universal de éxito. Su significado depende del resultado $R$ y de la dirección que se está intentando resolver. La misma configuración puede cerrar al corregir $R$, permanecer abierta al corregir $M$ o exigir deducir $B$. Por eso la notación canónica es $E_C$.

Cuando $R$ pertenece a $\{0, 1\}$, $E_C$ distingue tres situaciones relacionales: mayoría o cierre en la dirección ensayada; antimayoría o contradicción respecto de esa dirección; y estado no monótono o todavía abierto. La tabla exhaustiva de estos casos debe congelarse junto con la implementación, porque cambiar $C$ cambia la variable candidata y obliga a recalcular $E$.

Cuando $R = 2$, la regla ya está determinada: $E$ conserva el trit residual que no pertenece a la apertura mayoritaria. Si no existe un residual único, $E$ permanece en `2`.

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

La autorreferencia se excluye: ES no puede seleccionar como FN la misma posición desde la que se define. La tripleta $(0, 1, 2)$ es, por ello, un tensor imposible como cierre literal. Puede emerger como firma abierta de una relación, pero no constituye un objetivo impuesto ni una condición externa de aceptación.

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
| ES | $(ES_1, ES_2, ES_3)$ | $R \to DS[0],\; E \to DE[0],\; O \to DO[0]$ | Estructura |
| FN | $(FN_1, FN_2, FN_3)$ | $R \to DS[1],\; E \to DE[1],\; O \to DO[1]$ | Función |
| FO | $(FO_1^*, FO_2^*, FO_3^*)$ | $R \to DS[2],\; E \to DE[2],\; O \to DO[2]$ | Forma |

La tripleta de conocimiento se escribe en el orden operativo:

$$K = (DO,\; DE,\; DS)$$

$DO$ ocupa el papel estructural y orienta el recorrido; $DE$ ocupa el papel funcional y expresa el estado dependiente de la dirección; $DS$ ocupa el papel formal y contiene el resultado emergente. Así, $K$ vuelve a ser una tripleta ordenable y no un registro especial con tres campos externos.

> **Autosimilitud:** tres elementos ordenados producen tres relaciones; tres relaciones proyectan $(R, E, O)$; y esas proyecciones forman una nueva tripleta $(DO, DE, DS)$. TriGate, cara, tensor, transcender y ventana repiten esta operación a distinta escala.

---

## 5. El transcender: entrada, conocimiento y salida

El transcender aplica la misma cara a tres estructuras del mismo tipo: entrada $I$, conocimiento $K$ y salida $S$. No es un módulo distinto; es la operación mínima ejecutada sobre una escala superior:

$$\Phi(I, K, S;\; C, DO_t) \;\to\; (DO_{t+1},\; DE_C,\; DS)$$

La entrada actúa como evidencia. Cuando todavía no existe una memoria capaz de proponer otra cosa, la salida comienza como reflejo de la entrada: $S_0 = I$. A partir de ese estado, cada componente de $S$ debe proceder de $I$ o de una candidata recuperada del diccionario. Aurora no inventa una salida sin procedencia.

Una salida completa no significa una salida sin trits `2`. Significa que el paquete entero posee procedencia y puede reejecutarse. Un `2` puede permanecer cerrado si representa de forma coherente apertura, ausencia de relación, exterioridad o cualquier otro valor ternario legítimo.

Las tres caras de control operan canales homólogos de $I$, $K$ y $S$:

- **C4** opera $(DS_I,\; DS_K,\; DS_S)$.
- **C5** opera $(DE_I,\; DE_K,\; DE_S)$.
- **C6** opera $(DO_I,\; DO_K,\; DO_S)$.

C4, C5 y C6 no son controladores externos. Cada una es un sistema respecto de las tres unidades que recibe y, al mismo tiempo, un elemento de la capa superior. Cada cara produce su propio paquete:

$$C4 \to (DO_4, DE_4, DS_4)$$
$$C5 \to (DO_5, DE_5, DS_5)$$
$$C6 \to (DO_6, DE_6, DS_6)$$

Sus proyecciones homólogas forman tres nuevas tripletas:

$$HDS = (DS_4, DS_5, DS_6)$$
$$HDE = (DE_4, DE_5, DE_6)$$
$$HDO = (DO_4, DO_5, DO_6)$$

Tres TriGates ordinarios operan estas tripletas y producen el control emergente:

- $RD = R(HDS)$: `0` aprender; `1` inferir; `2` deducir o buscar.
- $RC = R(HDE)$: `0` incoherente; `1` coherente; `2` ambiguo.
- $RO = R(HDO)$: `0` buscar en el diccionario local; `1` buscar en la red Aurora; `2` detener.

Los patrones `0-1-2`, `1-1-1` y `0-0-0` no se imponen como invariantes del control ni se usan como destinos contra los que calcular una distancia. Pueden emerger como firmas de determinadas relaciones, pero la decisión procede únicamente de $RD$, $RC$ y $RO$. Tampoco se necesita una función Manhattan ni otro evaluador externo.

Inferir significa sintetizar el paquete y encontrar, mediante el conocimiento, una salida completa para el conjunto. Aprender reconstruye $M$ y conserva una relación nueva. Deducir reconstruye $B$ y es también la operación de búsqueda. Las tres acciones son las tres direcciones del mismo TriGate.

La regla autosimilar queda explícita: una unidad es sistema respecto de sus tres componentes y elemento respecto de la capa que la contiene. El control no está situado fuera de Aurora; emerge cuando los resultados de un nivel vuelven a convertirse en entradas del siguiente.

---

## 6. El control emergente como cara ordinaria

El nombre *semilla de armonización* describe únicamente el papel desempeñado por C4, C5 y C6. No designa una semilla especial. La misma secuencia que produce conocimiento en una cara inferior produce $RD$, $RC$ y $RO$ en la capa superior.

**$RD$ decide qué relación debe reconstruirse:**

- $RD = 0$: aprende reconstruyendo $M$.
- $RD = 1$: infiere reconstruyendo $R$ y sintetizando la salida.
- $RD = 2$: deduce o busca reconstruyendo $B$.

**$RC$ declara el estado de congruencia del resultado:**

- $RC = 0$: impide consolidar la candidata por incoherencia.
- $RC = 1$: permite aceptar la relación como coherente.
- $RC = 2$: conserva la ambigüedad y puede transportar carry.

**$RO$ determina el alcance de la búsqueda:**

- $RO = 0$: continúa dentro del diccionario local.
- $RO = 1$: eleva la consulta a la red, que es el diccionario de la capa superior.
- $RO = 2$: detiene la búsqueda.

Después de cada cambio se recalcula $E_C$. Por ello, una misma relación puede producir valores $E$ diferentes en aprendizaje, inferencia y deducción. Esta dependencia direccional replica exactamente la regla del TriGate.

### 6.1 Ciclo de realimentación

1. Tomar una fotografía estable de todas las caras de la ventana y del $DO$ vigente.
2. Reejecutar C4, C5 y C6 y obtener sus tres paquetes $(DO, DE, DS)$.
3. Proyectar $HDS$, $HDE$ y $HDO$ y operar cada tripleta con un TriGate ordinario.
4. Aplicar $RD$: aprender $M$, inferir $R$ o deducir $B$.
5. Aplicar $RC$: rechazar por incoherencia, aceptar por coherencia o conservar ambigüedad.
6. Cuando $RD$ requiere una candidata, aplicar $RO$: consultar el diccionario local, elevar la consulta a la red o detener.
7. Publicar las modificaciones como entradas del intento siguiente. Si la relación permanece abierta, transportar $DE$ junto con $DO$ como carry.

El ciclo se realimenta entre todas las semillas operativas de la ventana. Una modificación local vuelve a proyectar $DS$, $DE$ y $DO$; esos canales reactivan C4, C5 y C6; y el proceso continúa hasta obtener una decisión común para toda la ventana.

Parar y cerrar son decisiones distintas. $RO = 2$ termina el recorrido; $RC$ declara cómo termina:

- $(RC, RO) = (1, 2)$: cierre coherente.
- $(RC, RO) = (2, 2)$: parada ambigua o relación no resuelta.
- $(RC, RO) = (0, 2)$: detención por incoherencia o agotamiento sin solución válida.

### 6.2 Gasto y condición de parada

$DO$ es simultáneamente orientación, alcance y registro de iteración. Cada intento tiene coste porque consume un estado del recorrido. El sistema solo visita los estados admitidos por la sucesión canónica de búsqueda —planteada como recorrido Fibonacci en base tres— y no vuelve a probar un estado mientras el contexto no cambie.

La condición de parada no es una distancia numérica ni la presencia aislada de trits `2` en el contenido. La decisión aparece al operar el canal superior:

$$\text{detener} \iff R(HDO) = 2$$

Este resultado sintetiza el agotamiento del recorrido admisible. $R(HDO) = 0$ conserva la búsqueda local y $R(HDO) = 1$ cambia de escala sin introducir un mecanismo de encaminamiento distinto. La tabla exhaustiva de $E_C$, $O$ y del recorrido Fibonacci ternario debe codificarse y verificarse en el software, pero ya no exige añadir otro controlador a la arquitectura.

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

La ventana recibe tres tensores o tripletas del mismo nivel y los opera como una cara. Entrada, conocimiento y salida se realimentan mediante C4, C5 y C6 hasta producir una decisión para la ventana completa. $DO$ pertenece a la ventana durante este ciclo y no se reinicia en cada semilla operativa.

- **Cierre coherente:** cuando $RC = 1$ y $RO = 2$, emerge una unidad superior $(DO, DE, DS)$, se conserva la traza de sus tres descendientes y la unidad puede entrar en la siguiente escala.
- **Incoherencia:** cuando $RC = 0$, la alternativa no se consolida. Mientras $RO = 0$ se prueba otra candidata local; con $RO = 1$ la consulta asciende a la red; con $RO = 2$ termina sin solución válida.
- **Ambigüedad:** cuando $RC = 2$, $DE$ y su orientación $DO$ pueden transportarse como carry. El carry no es un resultado cerrado, sino una relación que necesita el siguiente contexto.
- **Alcance:** $RO = 0$ mantiene la búsqueda en la memoria local; $RO = 1$ eleva la misma consulta a la red; $RO = 2$ detiene el recorrido. La red no es una excepción a la ventana, sino la siguiente escala de la misma operación.

Todas las caras de una ventana usan una fotografía estable. Los cambios producidos durante un intento se publican para el intento siguiente. Esta separación $DO_t \to \text{operación } t \to DO_{t+1}$ evita dependencias circulares instantáneas y permite reproducir la ejecución.

Al finalizar un clúster, las unidades emergentes vuelven a agruparse de tres en tres y se repite el mismo proceso. No existe una operación especial de subida: la salida de una cara es la entrada de la siguiente.

---

## 9. El proceso de extensión

La extensión recorre el tensor en sentido descendente. No invierte una fórmula distinta: plantea la unidad que falta como $B$, aplica $C = 2$ y reejecuta con el mismo TriGate.

1. Usar $DS$ como parte de la relación deductiva, no como identidad única ni como clave de igualdad exacta.
2. Calcular $D(A, M, R)$ y recuperar primero las candidatas compatibles de la memoria temporal de la ventana.
3. Si $RO = 0$, continuar en el diccionario local. Si $RO = 1$, elevar la misma relación incompleta a la red. Si $RO = 2$, detener.
4. Ordenar las candidatas con $DO$ y comprobar su $DE$ en la dirección de reconstrucción.
5. Reejecutar la candidata dentro de la relación completa. Si cierra y es congruente, extenderla; si no, probar la siguiente.
6. Si ninguna candidata cierra y $RD = 0$, aprender una nueva relación y añadirla como competidora. Si $RO = 2$, conservar la clasificación final indicada por $RC$.

La extensión refleja la asimetría del TriGate. Cuando $R = 2$, $E$ y $O$ pueden conservar el residual y su orientación, permitiendo una reconstrucción estructural sin pérdida. Cuando $R$ pertenece a $\{0, 1\}$, la síntesis conserva la ley mayoritaria y el detalle que no quedó determinado reaparece como `2`. La extensión no inventa ese detalle: lo vuelve a declarar abierto.

La dirección depende del objeto reconstruido: extender una salida usa inferencia; reconstruir conocimiento usa aprendizaje; reconstruir una entrada abierta usa deducción. En cada caso se recalcula $E_C$.

---

## 10. El diccionario: encadenamiento, competencia y lexicalización

El diccionario es parte de la operación, no una memoria auxiliar separada. Conserva relaciones completas y reejecutables, no solamente resultados aislados. Su unidad mínima incluye entrada, conocimiento, salida y dirección:

$$U = (I,\; K,\; S,\; C)$$

La unidad conserva además su paquete emergente $(DO, DE, DS)$, su procedencia y las referencias necesarias para reproducir el cierre.

### 10.1 La salida de una cara entra en el diccionario

Cuando una semilla operativa recibe tres tripletas y su conocimiento aplicable, calcula una nueva tripleta $T'$. La relación que la produjo se almacena completa:

$$(T_1, T_2, T_3;\; K,\; C) \;\to\; U = (I, K, S = T', C)$$

El diccionario puede organizar familias mediante $DS$, $DE$, $DO$ y $C$, pero estas coordenadas no deciden por igualdad exacta. Solo reducen el espacio de candidatas. La validez se determina deduciendo, reejecutando y comprobando el cierre de la relación completa.

La salida no es efímera. Se convierte en una unidad reutilizable y puede encadenarse como entrada de otra cara. La misma relación puede conservar más de una salida o más de un conocimiento candidato; las alternativas compiten sin borrar las que siguen siendo válidas en otros contextos.

### 10.2 Búsqueda deductiva y competencia

Buscar en el diccionario es ejecutar el TriGate en dirección deductiva $C = 2$. $A$, $M$ y el resultado buscado $R$ forman la consulta; $B$ es el tensor que debe recuperarse:

$$D(A, M, R) = \{B \mid \text{Majority}_3(A, B, M) = R\}$$

Ejemplos: $D(0,2,0) = \{0\}$; $D(0,2,2) = \{1,2\}$; $D(1,2,1) = \{1\}$; $D(2,2,2) = \{0,1,2\}$.

- Si el dominio es vacío, esa familia no contiene solución.
- Si contiene un único $B$, la deducción recupera directamente la candidata.
- Si contiene varios $B$, las candidatas permanecen abiertas y compiten mediante reejecución, $RC$ y $DO$.

Cuando $RO = 0$, la deducción se resuelve en el diccionario local. $RO = 1$ no cambia de operador: eleva la relación incompleta al diccionario distribuido. $RO = 2$ detiene la búsqueda.

1. Reutilizar primero una candidata estructuralmente compatible que haya cerrado previamente en ese contexto.
2. Reejecutarla dentro de la cara y de la ventana actuales.
3. Si vuelve a cerrar, conservarla y actualizar su prioridad de uso.
4. Si no cierra, probar otra candidata sin eliminar la anterior.
5. Si ninguna cierra y $RD = 0$, aprender una nueva tripleta, almacenarla y hacerla competir con las anteriores.

La candidata anterior puede seguir siendo correcta en otro contexto. Aurora no sustituye globalmente una representación por otra: conserva ramas alternativas y deja que el cierre congruente seleccione la aplicable. El mismo proceso entre tripletas crea los tensores; entre tensores crea niveles superiores; y entre tensores de consulta y tensores de nodo organiza la red.

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

La red Aurora es el diccionario en la escala superior. Cuando $RO = 1$, el nodo local no ejecuta otro protocolo lógico: eleva la misma relación deductiva y busca como $B$ el tensor-identidad de un nodo capaz de completar la consulta:

$$\text{consulta no resuelta} \;\to\; \text{deducción del tensor de nodo} \;\to\; \text{reejecución remota} \;\to\; \text{verificación local}$$

Cada nodo adquiere y refina su tensor-identidad según las relaciones que ha ayudado a cerrar. Una respuesta válida aprende simultáneamente dos unidades: el conocimiento que resolvió la consulta y la relación entre esa consulta y el nodo que la resolvió. De este modo, los nombres de los nodos se ordenan semánticamente por su experiencia y especialización.

Si no existe una coincidencia exacta, Aurora no introduce una distancia vectorial externa. Extiende o descompone el tensor abierto y deduce el nodo asociado con la estructura compatible más específica. Las candidatas compiten mediante la misma reejecución, coherencia y recorrido $DO$ que los elementos del diccionario local.

El nodo seleccionado recibe la unidad abierta completa, no un token aislado. Inicia su resolución en su propio diccionario con $RO = 0$. Devuelve la candidata junto con $K = (DO, DE, DS)$, procedencia y traza suficiente para reejecutar el cierre. El nodo solicitante no acepta conocimiento por autoridad: lo verifica localmente antes de consolidarlo.

Las estructuras y rutas útiles ganan prioridad porque vuelven a cerrar y reducen gasto. Las que no ayudan pierden prioridad de consulta sin necesidad de borrarse inmediatamente. Así, especialización, encaminamiento, reputación operativa e intercambio de conocimiento reutilizan la misma competencia del diccionario.

---

## 12. Arranque del sistema

El conocimiento vacío se representa mediante una unidad cuyos trits son `2`: $K_0 = \bot$. El arranque no activa un generador especial de salida. Mientras el diccionario no aporte otra candidata, $S_0 = I$: entrada y salida comienzan como una relación reflexiva reejecutable.

Toda salida posterior debe satisfacer:

$$S \in \{I\} \cup \text{Salidas}(\text{diccionario local}) \cup \text{Salidas}(\text{red})$$

La relación inicial $(I, \bot, I)$ se opera como cualquier otra cara. Si $RD = 0$, produce una candidata de conocimiento; si $RD = 1$, sintetiza una salida con procedencia; si $RD = 2$, deduce el elemento que falta. La candidata entra en el diccionario y debe cerrar al ser reejecutada.

Por tanto, el primer conocimiento no aparece mediante la asignación especial $K \leftarrow I$. Aparece mediante la secuencia ordinaria:

$$\text{vacío} \to \text{cara} \to \text{candidata} \to \text{diccionario} \to \text{reejecución} \to \text{cierre o alternativa}$$

Si la candidata cierra, se reutiliza y puede formar estructuras superiores. Si no cierra, se aprende otra y ambas compiten. $RO$ decide si la búsqueda continúa localmente, asciende a la red o se detiene. El arranque, el aprendizaje continuo, la corrección y el encaminamiento usan exactamente el mismo proceso.

---

## 13. Ejecución distribuida mediante autómatas relacionales

Aurora se ejecuta como una red de relaciones activas. Cada TriGate conserva referencias a $A$, $B$, $M$, $R$, $E_C$ y $O$. Cuando cambia una celda, se reactivan únicamente las relaciones que la comparten:

$$\text{cambio} \;\to\; \text{TriGate} \;\to\; \text{cara} \;\to\; (DO, DE, DS) \;\to\; \text{relaciones dependientes}$$

No existe un procesador central que recorra todas las semillas. Una cara superior se activa por los mismos eventos que una cara inferior. C4, C5 y C6 son relaciones ordinarias; sus paquetes forman $HDS$, $HDE$ y $HDO$, cuyos $R$ deciden operación, coherencia y alcance.

### 13.1 Regla de actualización

1. Leer una fotografía estable de las celdas compartidas y del $DO$ vigente.
2. Aplicar la dirección $C$ y calcular la propuesta correspondiente.
3. Recalcular el paquete $(R, E_C, O)$ de cada TriGate afectado.
4. Proyectar los canales superiores $DS$, $DE_C$ y $DO_{t+1}$.
5. En el transcender, reagrupar las proyecciones de C4, C5 y C6 como $HDS$, $HDE$ y $HDO$, y calcular $RD$, $RC$ y $RO$.
6. Aplicar la única transición correspondiente: aprender, inferir o deducir; clasificar la coherencia; y mantener la búsqueda local, elevarla a red o detenerla.
7. Publicar un evento solo si el paquete ha cambiado.
8. Reejecutar las caras dependientes en el intento siguiente.

La regla $\Delta\mathcal{T} = 0 \Rightarrow \text{no emitir evento}$ concentra la actividad en las regiones afectadas. Los TriGates independientes pueden operar en paralelo; las relaciones dependientes avanzan cuando reciben una nueva fotografía coherente.

### 13.2 Histéresis, competencia y confluencia

Cada ventana conserva los estados $DO$ visitados y las candidatas ensayadas. Una alternativa fallida no se repite mientras el contexto no cambie. Si dos órdenes de eventos producen soluciones compatibles, deben converger en el mismo cierre; si representan soluciones legítimamente distintas, permanecen como ramas competidoras hasta que el contexto las resuelva.

### 13.3 Condiciones de detención

- $RO = 0$: continuar la deducción en el diccionario local.
- $RO = 1$: elevar la misma consulta deductiva a la red Aurora.
- $RO = 2$ y $RC = 1$: detener con cierre coherente y sintetizar.
- $RO = 2$ y $RC = 2$: detener como ambiguo o no resuelto, conservando carry cuando proceda.
- $RO = 2$ y $RC = 0$: detener por incoherencia o agotamiento sin solución válida.
- Ningún paquete cambia: punto fijo local. Su clasificación final depende igualmente de $RC$ y $RO$; la ausencia de eventos no se confunde con coherencia.

La secuencia operativa completa queda reducida a una sola pauta autosimilar:

> **ordenar → entrelazar → emerger → proyectar → deducir → reejecutar → reutilizar, aprender o elevar**

Los datos, el conocimiento, la orientación, el cierre y el control utilizan el mismo vocabulario ternario y la misma composición de caras. La diferencia entre niveles no reside en el operador, sino únicamente en el tipo de unidad que ocupa cada una de las tres posiciones.

Con esta unificación, la arquitectura conceptual queda cerrada. Diccionario, red, especialización y control no añaden operadores nuevos: son funciones y escalas del TriGate. El trabajo pendiente es de ingeniería y validación: completar el núcleo ejecutable, congelar mediante pruebas exhaustivas las tablas ternarias y crear los tensores canónicos de los tokens simples.

---

## A. Licencias

Aurora está licenciada bajo las licencias **Apache 2.0** y **CC BY 4.0**.

Esto significa que cualquier persona es libre de usar, modificar y redistribuir el modelo, siempre que se cumplan las siguientes condiciones:

1. Deben mantenerse los avisos originales de copyright y de licencia en cualquier versión modificada o redistribuida *(Apache 2.0)*.
2. Debe otorgarse crédito al proyecto original, Aurora, mencionando claramente su procedencia *(CC BY 4.0)*.

Al adoptar este enfoque de licenciamiento, buscamos garantizar que Aurora permanezca libre, abierta y accesible para todos. Este modelo fomenta la innovación y la colaboración, al mismo tiempo que protege el reconocimiento y la integridad del proyecto.
