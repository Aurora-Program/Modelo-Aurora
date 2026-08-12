# El diccionario de Aurora

## Una memoria asociativa ternaria que navega el conocimiento de arriba abajo

En una arquitectura convencional, buscar información suele significar conocer de antemano dónde está almacenada. Una dirección conduce a una posición de memoria y esa posición devuelve un contenido. La dirección y el conocimiento son dos cosas diferentes.

Aurora propone otra posibilidad: que la propia estructura de aquello que se busca actúe como camino de acceso.

El sistema no pregunta «¿en qué dirección está este tensor?», sino «¿qué regiones del diccionario son compatibles con esta geometría?». La consulta activa primero las síntesis superiores más próximas y, desde ellas, desciende por un grafo de relaciones hasta encontrar un token completo que cierre con el tensor buscado.

Esta idea convierte el diccionario en algo más que una colección de tensores. Lo convierte en una **memoria asociativa ternaria, jerárquica y autoindexada**: la misma estructura fractal que conserva el conocimiento permite también llegar hasta él.

## Del direccionamiento a la compatibilidad

Aurora utiliza tres valores:

\[
\{0,1,2\}
\]

Los valores `0` y `1` representan determinaciones complementarias. El valor `2` representa apertura: una dimensión desconocida, todavía no resuelta o situada fuera del espacio determinado por la relación actual.

En una búsqueda del diccionario, estos valores no se comparan mediante igualdad simétrica. La consulta define una relación direccional de compatibilidad:

\[
0\rightarrow\{0\}
\]

\[
1\rightarrow\{1\}
\]

\[
2\rightarrow\{0,1,2\}
\]

Por tanto, buscar `0` exige encontrar `0`, y buscar `1` exige encontrar `1`. En cambio, buscar `2` permite continuar por cualquiera de los tres valores, porque esa posición de la consulta todavía no impone una determinación.

Podemos expresarlo así:

\[
q\sim d
\iff
q=2\;\lor\;q=d
\]

donde \(q\) es el trit de la consulta y \(d\) es el trit almacenado en el diccionario.

Esta relación es intencionadamente asimétrica. Un `2` en la consulta acepta `0`, `1` o `2`; un `2` almacenado no satisface por sí solo una consulta determinada como `0` o `1`. La apertura pertenece a quien pregunta, no sustituye una respuesta que la consulta ya ha fijado.

## El TriGate como comparador elemental

La comparación puede realizarse con el mismo TriGate que opera el resto de Aurora. Para cada posición se configura:

\[
T(A=q,\;B=d,\;M=2;\;R=q,\;C=0,\;E_C)
\]

donde:

- \(q\) es el trit buscado;
- \(d\) es el trit leído del diccionario;
- \(A=R=q\) duplica la consulta y la utiliza como ancla;
- \(M=2\) mantiene abierto el espacio de compatibilidad;
- \(C=0\) orienta la comprobación hacia \(B\), el valor almacenado;
- \(E_C=0\) indica que no queda separación entre el candidato concreto y la restricción de búsqueda.

El resultado local es:

| Consulta \(q\) | Trit almacenado \(d\) | Estado |
|---:|---:|---|
| 0 | 0 | Compatible: \(E_C=0\) |
| 0 | 1 o 2 | No compatible |
| 1 | 1 | Compatible: \(E_C=0\) |
| 1 | 0 o 2 | No compatible |
| 2 | 0, 1 o 2 | Compatible: \(E_C=0\) |

Aquí aparece una precisión importante. En otras operaciones de Aurora, \(R=2\) puede señalar un resultado aún abierto y \(E\) transporta el residuo que permitirá resolverlo después. En la búsqueda, sin embargo, \(R\) contiene una **restricción fija** y la dirección \(C=0\) comprueba un candidato concreto en \(B\). Por eso una consulta `2` puede cerrar localmente con cualquiera de los tres valores.

El significado no depende únicamente del símbolo `2`, sino de la posición que ocupa y de la dirección en la que se está recorriendo la relación.

## Un cierre local no elige una única rama

Cuando la consulta contiene `0` o `1`, el tipo de rama compatible queda determinado. Cuando contiene `2`, pueden cerrar varias ramas al mismo tiempo.

Esto obliga a distinguir dos hechos:

\[
E_C=0
\]

significa que **una candidata concreta es compatible**, mientras que:

\[
\#\text{candidatas compatibles}>1
\]

significa que la navegación todavía dispone de varias rutas posibles.

La multiplicidad de caminos no convierte en incoherente cada comparación local. Varios candidatos pueden ser válidos en una dimensión y, sin embargo, solo uno de sus recorridos permitir reconstruir el tensor completo. La selección definitiva no se decide en un trit aislado, sino mediante el cierre de toda la estructura.

## Por qué la búsqueda comienza en la cima

Los tensores de Aurora se organizan fractalmente:

\[
1\rightarrow3\rightarrow9\rightarrow27\rightarrow\cdots
\]

Cada unidad superior sintetiza la relación entre tres unidades inferiores y conserva su procedencia. Por tanto, una dimensión superior no contiene necesariamente todos los detalles inferiores como una lista plana, pero sí representa una relación de mayor alcance.

Esa síntesis tiene una importancia computacional especial: una decisión tomada en la cima orienta regiones cada vez más amplias del grafo.

Por esta razón, la recuperación no debería comenzar comparando todos los trits de todos los tensores almacenados. Debería comenzar por las dimensiones más sintetizadas:

\[
\text{síntesis superior}
\rightarrow
\text{Semilla Operativa}
\rightarrow
\text{tripleta}
\rightarrow
\text{trit}
\]

En cada nivel, el trit o la unidad buscada ordena los descendientes compatibles. La candidata de mayor prioridad se visita primero. Si su recorrido no permite completar el tensor, el sistema asciende hasta la última bifurcación y prueba la siguiente candidata.

La cima no demuestra por sí sola cuál es el destino correcto. Su función es decidir **qué camino merece ser intentado antes**.

## Un grafo con tres destinos por nodo

La búsqueda no consiste únicamente en seguir una cadena hasta una hoja. Cada nodo superior procede de tres unidades inferiores y, para reconstruirlo, deben alcanzarse sus tres destinos.

Si un nodo buscado es:

\[
Q=(q_0,q_1,q_2)
\]

el nodo solo queda completo cuando cada uno de sus tres componentes ha encontrado un descendiente compatible:

\[
\operatorname{cierre}(Q)=0
\iff
\forall i\in\{0,1,2\},\;
\exists d\in L_i:\;q_i\sim d
\]

donde \(L_i\) es la lista ordenada de candidatas disponibles para el destino \(q_i\).

La estructura combina así dos tipos de condición:

- una condición **AND**, porque deben cerrarse los tres destinos del nodo;
- una condición **OR**, porque cada destino puede disponer de varias candidatas compatibles.

Por eso el diccionario se entiende mejor como un **grafo AND–OR ternario** que como un árbol de decisión convencional. Distintas estructuras superiores pueden compartir descendientes, y una misma síntesis puede conservar varias representaciones que compiten en contextos diferentes.

## Prioridad sin eliminación

El aspecto decisivo del mecanismo es que Aurora no necesita eliminar una rama solo porque otra parezca mejor desde la cima.

Las dimensiones superiores establecen una prioridad. No dictan una exclusión irreversible.

El recorrido básico sería:

1. Comparar la consulta con las síntesis superiores disponibles.
2. Reunir las candidatas compatibles para el primer destino.
3. Ordenarlas por prioridad.
4. Descender por la candidata mejor situada.
5. Intentar completar sus tres destinos inferiores.
6. Confirmar los nodos que cierren y continuar con el siguiente destino pendiente.
7. Si la ruta no puede completar el tensor, volver a la bifurcación más cercana.
8. Probar la siguiente candidata de menor prioridad.
9. Continuar hasta encontrar un token completo compatible o agotar todas las alternativas admisibles.

Una prioridad equivocada no hace perder la solución. Solo incrementa el gasto necesario para encontrarla.

Esta propiedad separa la **corrección** de la **eficiencia**:

- conservar las alternativas y retroceder garantiza una búsqueda completa;
- ordenar bien las alternativas reduce el número de recorridos necesarios.

## De dónde procede la prioridad

Cuando la consulta está determinada por `0` o `1`, la compatibilidad reduce mucho el espacio. Cuando aparece `2`, pueden quedar abiertas varias rutas y es necesario decidir cuál explorar primero.

La prioridad puede construirse con información que Aurora ya conserva:

- \(DS\), como síntesis y localizador de una familia de estructuras;
- \(DE\), como historial de cierre en una dirección comparable;
- \(DO\), como orientación, recorrido y gasto de búsqueda;
- \(O\), como posición o sentido de lectura;
- la memoria temporal de la ventana actual;
- el último uso exitoso de una candidata;
- los contextos en los que esa candidata cerró anteriormente;
- el coste que exigieron sus recorridos previos.

El diccionario no necesita reducir todas estas señales a una dirección rígida. Puede mantener una lista ordenada de candidatas que se actualiza con la experiencia.

Una estructura que vuelve a cerrar gana prioridad. Una que obliga a retroceder repetidamente la pierde, pero no se borra: puede seguir siendo correcta en otro contexto.

Así emerge también la especialización. Dos nodos pueden compartir los mismos tensores y, sin embargo, ordenar de forma distinta sus diccionarios según su experiencia. El conocimiento continúa siendo interoperable, mientras que la ruta preferida se adapta localmente.

## El papel de DO en el retroceso

Para retroceder sin reiniciar toda la operación, cada estado de búsqueda debe conservar al menos:

\[
S_k=(N_k,i_k,L_k,P_k)
\]

donde:

- \(N_k\) es el nodo actual;
- \(i_k\) identifica cuál de sus tres destinos se está resolviendo;
- \(L_k\) contiene las candidatas ordenadas;
- \(P_k\) registra cuáles ya han sido probadas.

En términos operativos:

\[
\text{fallo}
\rightarrow
\text{ascenso localizado}
\rightarrow
\text{siguiente prioridad}
\rightarrow
\text{nuevo descenso}
\]

\(DO\) puede representar este gasto y evitar que el sistema repita un estado mientras el contexto no haya cambiado. Si ya no existe ninguna alternativa admisible, la búsqueda se detiene y conserva la entrada como no resuelta, en lugar de inventar un cierre.

## Dos movimientos complementarios

La arquitectura distingue dos recorridos que pueden parecer opuestos, pero forman parte del mismo mecanismo.

### Síntesis ascendente

Durante el aprendizaje y la construcción del tensor, los cierres locales forman estructuras cada vez mayores:

\[
\text{trit}
\rightarrow
\text{tripleta}
\rightarrow
\text{Semilla Operativa}
\rightarrow
\text{tensor}
\]

El ascenso crea conocimiento comprimido y conserva la procedencia que lo originó.

### Navegación descendente

Durante la recuperación, la síntesis superior actúa como entrada al grafo:

\[
\text{tensor}
\rightarrow
\text{Semilla Operativa}
\rightarrow
\text{tripleta}
\rightarrow
\text{trit}
\]

El descenso localiza las relaciones inferiores relevantes.

Finalmente, el candidato encontrado se reejecuta y su cierre se confirma desde las relaciones elementales hacia la unidad completa. En otras palabras:

> La síntesis ascendente construye el índice; la navegación descendente recupera el candidato; la reejecución ascendente verifica que el candidato sigue cerrando en el contexto actual.

## Encontrar no es aceptar

Alcanzar un tensor compatible no significa que Aurora deba incorporarlo automáticamente como conocimiento válido.

El diccionario recupera candidatos creados o aprendidos anteriormente. Después, la candidata debe volver a operar dentro de la cara y de la ventana actuales. Solo si la relación completa produce cierre puede reutilizarse y actualizar su prioridad.

También pueden alcanzarse varios tokens completos compatibles. En ese caso, el diccionario no tiene que fingir una identidad única: devuelve candidatas ordenadas para que compitan en la ventana. En la lectura léxica puede ensayarse primero el token complejo más largo y, entre estructuras equivalentes, el utilizado con éxito más recientemente. Si esa segmentación no cierra, el sistema retrocede y prueba una unidad menor o una representación alternativa.

El ciclo es:

\[
\text{consultar}
\rightarrow
\text{navegar}
\rightarrow
\text{recuperar}
\rightarrow
\text{reejecutar}
\rightarrow
\text{cerrar o retroceder}
\]

Si ninguna candidata almacenada cierra y todavía queda gasto, el sistema puede calcular una nueva alternativa y añadirla al mismo espacio de búsqueda. La candidata anterior no se destruye, porque puede continuar siendo válida bajo otra orientación o en otro contexto.

De esta forma, aprender y recuperar no son procesos separados: ambos participan en una competencia continua entre estructuras reejecutables.

## Una visión cercana al hardware

El mecanismo puede imaginarse físicamente como una memoria asociativa ternaria con líneas locales de compatibilidad.

Cada TriGate compara un trit de la consulta con un trit almacenado. Los cierres locales habilitan caminos hacia el nivel inferior. Los nodos superiores ordenan esas señales y activan primero la región de mayor prioridad. Cuando una ruta falla, el estado de recorrido permite reactivar la siguiente sin explorar de nuevo todo el espacio.

No existe necesariamente una dirección numérica externa que identifique cada tensor. El propio patrón buscado abre caminos dentro de la memoria.

En esta visión, la estructura fractal cumple simultáneamente dos funciones:

### Memoria

\[
S
\leftarrow
(s_0,s_1,s_2)
\leftarrow
(x_0,x_1,\ldots)
\]

Conserva qué relaciones produjeron cada síntesis.

### Índice

\[
S
\rightarrow
s_i
\rightarrow
x_{ij}
\]

Conserva cómo volver a acceder a ellas.

Aurora no almacena únicamente lo que sabe. Al preservar síntesis, orientación, coherencia, gasto y procedencia, almacena también **cómo llegar hasta ese conocimiento y cómo volver a comprobarlo**.

## Eficiencia y límite combinatorio

Si la mayoría de las decisiones superiores están determinadas, la búsqueda puede recorrer una fracción muy pequeña del diccionario. En el caso ideal, su coste se aproxima a la profundidad del tensor, no al número total de tensores almacenados.

Sin embargo, cada `2` puede abrir varias candidatas. Si existen \(k\) bifurcaciones completamente abiertas, el peor caso mantiene una expansión combinatoria próxima a:

\[
O(3^k)
\]

Aurora no elimina ese límite por definición. Intenta hacer que resulte excepcional mediante síntesis informativas, prioridad contextual, reutilización de cierres anteriores y retrocesos localizados.

La hipótesis de eficiencia puede medirse con variables concretas:

- porcentaje del diccionario visitado por consulta;
- número medio de candidatas por destino;
- profundidad alcanzada antes de cada retroceso;
- cantidad de retrocesos necesarios para cerrar un token;
- coste de reejecutar una candidata frente al de reconstruirla;
- frecuencia con la que la primera ruta priorizada produce cierre.

La arquitectura es viable como algoritmo de búsqueda completo. Su ventaja computacional frente a otros índices deberá demostrarse mediante implementación y experimentación.

## Conclusión

El diccionario de Aurora no se limita a relacionar una clave con un valor. Organiza el conocimiento como un grafo fractal en el que cada síntesis superior resume una relación y, al mismo tiempo, abre un camino hacia las estructuras que la produjeron.

La consulta se expresa en el mismo lenguaje ternario que el conocimiento. `0` y `1` exigen determinación; `2` mantiene abierto el espacio. El TriGate comprueba cada compatibilidad local. Las dimensiones superiores establecen la prioridad del descenso. Cada nodo debe completar tres destinos. Y cuando una ruta no alcanza un tensor completo, el sistema retrocede y prueba la siguiente alternativa sin destruir la anterior.

Así, la eficiencia no depende de adivinar siempre el camino correcto. Depende de organizar el conocimiento para que las rutas más prometedoras se intenten primero, los errores puedan corregirse de forma localizada y cada estructura recuperada pueda volver a demostrar su cierre.

La idea central puede resumirse en una frase:

> En Aurora, el conocimiento no se recupera proporcionando su dirección; se recupera dejando que la geometría de la consulta encuentre, recorra y verifique su propio camino dentro del diccionario.
