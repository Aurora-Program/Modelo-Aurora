# Aurora: del lenguaje natural a la computación mínima

## Especificación can# Aurora: del lenguaje natural a la computación mínima

## Especificación canónica del núcleo relacional

**Versión:** 1.0  
**Fecha:** 9 de agosto de 2026  
**Estado:** arquitectura cerrada; referencia normativa para formalización, implementación y pruebas  
**Proyecto:** Aurora

---

## 0. Propósito y alcance

Aurora investiga una arquitectura de inteligencia artificial discreta, autosimilar y homoicónica. Su hipótesis es que datos, conocimiento, búsqueda, memoria y control pueden representarse mediante la misma clase de estructura ternaria y operarse con un único mecanismo relacional.

El objetivo no es construir un modelo probabilístico más pequeño, sino una máquina capaz de:

- aprender de forma local y continua;
- reutilizar conocimiento ya validado;
- buscar relaciones sin reconstruirlas estadísticamente en cada uso;
- compartir unidades de conocimiento verificables entre nodos;
- hacer emerger estructuras superiores mediante cierre;
- conservar como *carry* aquello que todavía necesita contexto.

Este documento define el núcleo canónico desde el TriGate hasta la ventana y el diccionario. Las explicaciones históricas, métricas de prototipos anteriores y variantes abandonadas no son normativas.

La jerarquía ejecutiva es:

\[
\boxed{
\text{TriGate}
\rightarrow
\text{cara}
\rightarrow
\text{transcender}
\rightarrow
\text{ventana}
\rightarrow
\text{diccionario}
}
\]

Cada nivel reutiliza la misma operación. Lo que cambia es el tipo de unidad que ocupa cada posición.

---

## 1. Vocabulario ternario e invariantes

### 1.1 Trit

Aurora usa el conjunto:

\[
\mathbb T=\{0,1,2\}
\]

- \(0\) y \(1\) son determinaciones complementarias.
- \(2\) representa apertura, indeterminación o valor todavía no resoluble en la relación actual.

En el orden parcial de información:

\[
2\sqsubseteq0,
\qquad
2\sqsubseteq1
\]

Resolver un \(2\) añade determinación. Mantenerlo conserva posibilidades.

### 1.2 Tripleta y tensor

Una tripleta es:

\[
P=(p_0,p_1,p_2),
\qquad p_i\in\mathbb T
\]

La construcción es recursiva:

\[
\mathcal T_0=\mathbb T,
\qquad
\mathcal T_{n+1}=\mathcal T_n^3
\]

Por tanto, un tensor Aurora no requiere otro operador: es una composición de tres unidades del nivel inferior.

### 1.3 Invariantes canónicas

Toda implementación debe conservar estas invariantes:

1. **Ternariedad:** el núcleo no introduce valores continuos para decidir cierre, búsqueda o control.
2. **Autosimilitud:** tres unidades del mismo nivel se operan mediante la misma forma relacional.
3. **Homoiconicidad:** una tripleta puede actuar como dato, conocimiento, índice, operación o control según su posición.
4. **Procedencia:** una unidad emergente conserva información suficiente para reordenarse y reejecutarse.
5. **Fotografía estable:** el estado producido en el intento \(t\) solo se aplica en \(t+1\).
6. **No creación durante la consulta:** una búsqueda fallida no inserta un tensor nuevo en el diccionario.
7. **Decisión local:** una SO modifica relaciones compartidas; no emite comandos externos a otro mecanismo.
8. **Propagación separada de construcción:** las SO locales construyen el estado; la ventana solo decide cómo se propaga.

---

## 2. El TriGate

### 2.1 Relación mínima

Un TriGate contiene:

\[
G=(A,B,M;R,E_C,O)
\]

donde:

| Símbolo | Papel |
|---|---|
| \(A\) | ancla de la relación |
| \(B\) | segundo operando |
| \(M\) | modo o función ternaria |
| \(R\) | resultado de la relación |
| \(E_C\) | estado relacional en la dirección \(C\) |
| \(O\) | orientación y siguiente recorrido |

El TriGate no debe interpretarse como una puerta de una sola dirección. Es una relación que puede recorrerse para resolver distintas posiciones.

### 2.2 Mayoría ternaria

La relación directa es:

\[
\widehat R=\operatorname{Maj}_3(A,B,M)
\]

con:

\[
\operatorname{Maj}_3(x,y,z)=
\begin{cases}
x,&x=y\ \lor\ x=z\\
y,&y=z\\
2,&x,y,z\ \text{son todos distintos}
\end{cases}
\]

Así, \(M=0\) se comporta como el sesgo conjuntivo, \(M=1\) como el sesgo disyuntivo y \(M=2\) conserva apertura cuando no aparece una mayoría determinada.

### 2.3 Dirección de resolución

La dirección \(C\) selecciona la celda transformable. \(A\) permanece como ancla.

| \(C\) | Celda resoluble | Operación |
|---:|---|---|
| \(0\) | \(B\) | deducción |
| \(1\) | \(R\) | inferencia |
| \(2\) | \(M\) | aprendizaje |

Inferir, deducir y aprender no son tres algoritmos. Son tres recorridos de la misma relación.

Para una dirección \(C\), el TriGate obtiene el conjunto de valores compatibles de la celda seleccionada:

\[
\mathcal S_C=
\{x\in\mathbb T:\operatorname{Maj}_3(A,B,M)=R\}
\]

sustituyendo por \(x\) la celda indicada por \(C\). Si existe más de una solución, \(O\) y el recorrido vigente determinan cuál se prueba; si todavía no puede elegirse una sin perder alternativas, la celda permanece en \(2\).

### 2.4 Emergencia \(E_C\)

\(E_C\) no es una votación adicional. Se recalcula después de operar en la dirección \(C\).

Sea:

\[
q=\operatorname{Maj}_3(A,B,M)
\]

Cuando \(R\in\{0,1\}\):

\[
E_C=
\begin{cases}
1,&q=R\\
0,&q\in\{0,1\}\ \land\ q\ne R\\
2,&q=2
\end{cases}
\]

Por tanto:

- \(E_C=1\): cierre coherente en la dirección ensayada;
- \(E_C=0\): contradicción o cierre complementario;
- \(E_C=2\): relación todavía abierta.

Cuando \(R=2\), \(E_C\) conserva el residual de la apertura:

| Configuración de \((A,B,M)\) | \(R\) | \(E_C\) |
|---|---:|---:|
| permutación de \((2,2,1)\) | \(2\) | \(1\) |
| permutación de \((2,2,0)\) | \(2\) | \(0\) |
| \((2,2,2)\) | \(2\) | \(2\) |
| permutación de \((0,1,2)\) | \(2\) | \(2\) |

Los dos últimos casos comparten \((R,E_C)=(2,2)\), pero no la misma procedencia. \(O\) los distingue.

### 2.5 Paquete observable

La salida completa del TriGate es:

\[
\operatorname{out}(G)=(R,E_C,O)
\]

Ninguno de sus componentes debe interpretarse aisladamente:

- \(R\) indica cierre o apertura del resultado;
- \(E_C\) califica ese estado o conserva su residual;
- \(O\) conserva desde dónde se leyó y cómo continuar.

---

## 3. Ordenación de una tripleta

### 3.1 Papeles ES, FN y FO

Ordenar no significa ordenar numéricamente. Significa asignar papeles relacionales:

- \(ES\): estructura;
- \(FN\): función;
- \(FO\): forma;
- \(O\): posición desde la que se lee la tripleta.

Para \(P=(p_0,p_1,p_2)\) y una orientación candidata \(o\):

\[
i_{ES}=o
\]

\[
ES=p_{i_{ES}}
\]

El valor de \(ES\) señala el índice de \(FN\):

\[
i_{FN}=ES
\]

La autorreferencia está prohibida:

\[
i_{FN}\ne i_{ES}
\]

El índice restante es \(i_{FO}\), y entonces:

\[
FN=p_{i_{FN}},
\qquad
FO=p_{i_{FO}}
\]

Una orientación es válida si no produce autorreferencia. Si existen varias, el estado vigente de \(DO\) selecciona la siguiente no visitada.

### 3.2 Tensor imposible y propósito abierto

En \((0,1,2)\), cada posición se señala a sí misma. Por ello, no existe una orientación literal válida:

\[
\operatorname{order}(0,1,2)=\varnothing
\]

La tripleta puede utilizarse como propósito abierto que mantiene la búsqueda orientada, pero no como cierre estructural literal.

### 3.3 Procedencia vertical

Cuando tres unidades forman otra superior:

\[
ES^{\uparrow}
=
ES_{\text{unidad inferior cuyo índice es }O^{\uparrow}}
\]

La orientación superior selecciona una relación inferior y conserva su estructura sin añadir un direccionador externo.

---

## 4. La cara

### 4.1 Entrada canónica

Una cara recibe tres tripletas del mismo nivel, procedentes de los tres tensores de la ventana:

\[
P_A,
\qquad
P_B,
\qquad
P_U
\]

\(A\) y \(B\) contienen contexto admitido. \(U\) es el tercer tensor abierto y comienza, en cada nueva ventana, con todos sus valores en \(2\):

\[
P_{U,0}=(2,2,2)
\]

La tercera tripleta no es un tercer token observado. Es la porción local de la búsqueda que todavía debe resolverse.

### 4.2 Dos familias entrelazadas de TriGates

La cara contiene dos familias con procedencias distintas.

#### A. TriGates de ordenación

Cada tripleta se ordena independientemente:

\[
Q_X(P_X)=(ES_X,FN_X,FO_X,O_X),
\qquad
X\in\{A,B,U\}
\]

Sus orientaciones forman:

\[
\boxed{DO=(O_A,O_B,O_U)}
\]

\(DO\) conserva cómo fueron leídos los tres tensores.

#### B. TriGates relacionales

Después de ordenar, se operan las coordenadas homólogas:

\[
G_{ES}=(ES_A,ES_B,ES_U)
\]

\[
G_{FN}=(FN_A,FN_B,FN_U)
\]

\[
G_{FO}=(FO_A,FO_B,FO_U)
\]

Cada grupo produce \((R,E_C,O)\), pero la cara proyecta canónicamente:

\[
\boxed{DS=(R_{ES},R_{FN},R_{FO})}
\]

\[
\boxed{DE_C=(E_{ES,C},E_{FN,C},E_{FO,C})}
\]

La procedencia normativa es, por tanto:

\[
\boxed{
\text{ordenación}\rightarrow DO
\qquad
\text{relación}\rightarrow(DE,DS)
}
\]

Los \(O\) internos de \(G_{ES}\), \(G_{FN}\) y \(G_{FO}\) pueden orientar la reejecución de esos TriGates, pero no sustituyen el \(DO\) canónico de la cara.

### 4.3 Conocimiento de cara

La salida completa se escribe en orden operativo:

\[
K=(DO,DE,DS)
\]

| Canal | Procedencia | Significado |
|---|---|---|
| \(DO\) | orientaciones de \(P_A,P_B,P_U\) | orden y recorrido |
| \(DE\) | emergencias de \(G_{ES},G_{FN},G_{FO}\) | estado relacional |
| \(DS\) | resultados de \(G_{ES},G_{FN},G_{FO}\) | síntesis local |

\(K\) no es un registro externo. Es otra tripleta Aurora. Puede ordenarse y entrar en una cara superior, donde producirá su propio \(DS^{\uparrow}\).

### 4.4 Fotografía estable

La cara lee \(DO_t\), ejecuta el intento y publica \(DO_{t+1}\):

\[
DO_t
\rightarrow
\operatorname{cara}_t
\rightarrow
DO_{t+1}
\]

\(DO_{t+1}\) nunca modifica retrospectivamente el intento que lo produjo.

---

## 5. Semilla operativa y evolución de U

### 5.1 La semilla operativa

Una semilla operativa, \(SO\), es una relación Aurora ordinaria que reúne el estado producido por las caras conectadas. No interpreta sus salidas para generar órdenes externas.

Su operación cambia celdas compartidas:

\[
\operatorname{SO}
\rightarrow
\text{nuevo estado relacional}
\rightarrow
\text{reactivación de las relaciones dependientes}
\]

El control es, por ello, información operada mediante el mismo mecanismo que los datos.

### 5.2 Tres representaciones del mismo desconocido

En la rama de salida deben identificarse como aspectos de un mismo proceso:

1. la tercera tripleta local \(P_U\);
2. la SO de salida \(SO_U\);
3. el tensor abierto \(U\) de la ventana.

No son tres objetos de conocimiento independientes. Son tres escalas de la misma consulta mientras se determina:

\[
U_0
\rightarrow
U_1
\rightarrow
\cdots
\rightarrow
U^*
\]

Cada actualización local añade restricciones a la búsqueda. No acuña un tensor.

### 5.3 Interpretación como índice parcial

Sea \(D\) el diccionario y \(D(U_i)\) el conjunto de entradas compatibles con el estado parcial de \(U_i\). La resolución progresa idealmente como:

\[
D(U_0)
\supseteq
D(U_1)
\supseteq
\cdots
\supseteq
D(U^*)
\]

Un paso puede mantener el conjunto si todavía no añade información, pero no debe ampliarlo sin que cambie el contexto o se retroceda explícitamente a otra rama.

---

## 6. El transcender

### 6.1 Escala de entrada, conocimiento y salida

El transcender relaciona tres unidades del mismo tipo:

\[
I=\text{entrada},
\qquad
K=\text{conocimiento},
\qquad
S=\text{salida}
\]

Cada unidad conserva:

- su tripleta ordenable \((ES,FN,FO)\);
- su conocimiento asociado \((DO,DE,DS)\).

La salida comienza abierta cuando todavía no existe una coincidencia seleccionada:

\[
S_0=(2,2,2)
\]

### 6.2 Caras C4, C5 y C6

C4, C5 y C6 pertenecen al transcender, no a la ventana.

| Cara | Canales relacionados | Proyección superior | Papel |
|---|---|---|---|
| C4 | \((DS_I,DS_K,DS_S)\) | \(R^{\uparrow}\) | resultado |
| C5 | \((DE_I,DE_K,DE_S)\) | \(E^{\uparrow}\) | coherencia o residual |
| C6 | \((DO_I,DO_K,DO_S)\) | \(O^{\uparrow}\) | orden y continuación |

En forma compacta:

\[
\boxed{
C4\equiv R^{\uparrow},
\qquad
C5\equiv E^{\uparrow},
\qquad
C6\equiv O^{\uparrow}
}
\]

Sus tres estados se relacionan mediante la misma operación y forman la semilla operativa del transcender:

\[
SO_X=\Phi(C4_X,C5_X,C6_X)
\]

### 6.3 Lectura jerárquica de C4 y C5

Primero se interpreta C4.

Si:

\[
R^{\uparrow}=2
\]

la relación del transcender sigue abierta. C5 conserva entonces el residual que participa en el carry local:

\[
C4=2
\quad\Longrightarrow\quad
C5=\text{estado relacional pendiente}
\]

Si:

\[
R^{\uparrow}\in\{0,1\}
\]

C5 recupera su función de evaluación:

\[
C4\ne2
\quad\Longrightarrow\quad
C5=\text{coherencia del cierre}
\]

C6 conserva la orientación desde la que se obtuvo cualquiera de los dos estados.

### 6.4 Límite de la decisión local

Una apertura en C4 de un solo transcender no decide por sí misma el movimiento de toda la ventana. Solo queda incorporada a \(SO_X\). La decisión global se produce un nivel después.

---

## 7. La ventana

### 7.1 Composición

La ventana opera tres tensores del mismo nivel:

\[
W_i=(A_i,B_i,U_i)
\]

- \(A_i\) y \(B_i\) proceden del clúster tensorial o de la propagación anterior.
- \(U_i\) es la consulta abierta, con la misma forma y nivel que \(A_i\) y \(B_i\).
- Al abrir una ventana nueva:

\[
U_0=(2,2,\ldots,2)
\]

Cada tensor posee su transcender y su SO:

\[
SO_A,
\qquad
SO_B,
\qquad
SO_U
\]

### 7.2 Semilla operativa de ventana

La ventana no se decide directamente mediante C4, C5 y C6. Relaciona las tres semillas ya construidas:

\[
\boxed{
SO_W=\Phi(SO_A,SO_B,SO_U)
}
\]

La proyección superior de \(SO_W\) produce:

\[
(R_W,E_W,O_W)
\]

Este paquete decide únicamente la propagación del estado inferior. No vuelve a construirlo.

### 7.3 Tabla canónica de transición

La lectura es jerárquica: primero \(R_W\); si ha cerrado, \(E_W\); \(O_W\) orienta el siguiente intento.

| \(R_W\) | \(E_W\) | Condición adicional | Acción de la ventana |
|---:|---:|---|---|
| \(2\) | cualquiera | relación abierta | transportar \(U_i^*\) completo como carry |
| \(0\) o \(1\) | \(1\) | cierre congruente | emerger verticalmente la unidad ya construida |
| \(0\) o \(1\) | \(0\) | incoherencia concluyente | no sintetizar \(A_i\) con \(B_i\); desplazar la ventana |
| \(0\) o \(1\) | \(2\) | queda \(DO\) admisible | continuar en la orientación \(O_W\) |
| cualquiera | cualquiera | recorrido agotado y ninguna decisión anterior | conservar el estado y marcar no resuelto |

La prioridad semántica es:

\[
\boxed{
R_W
\rightarrow
E_W
\rightarrow
O_W
\rightarrow
\text{gasto}
}
\]

El agotamiento se consulta únicamente cuando el paquete todavía exige otro intento. Un cierre, una incoherencia concluyente o un carry ya determinados no se revierten por haber consumido el último estado del recorrido.

### 7.4 Emergencia coherente

Si \(R_W\ne2\) y \(E_W=1\), la ventana reconoce que la estructura construida por las SO locales puede ascender:

\[
W_i
\rightarrow
T_i^{\uparrow}
\]

\(T_i^{\uparrow}\) conserva la procedencia de \(A_i\), \(B_i\), la coincidencia recuperada para \(U_i\) y sus paquetes \((DO,DE,DS)\).

La ventana no calcula de nuevo \(T_i^{\uparrow}\). Solo habilita su movimiento vertical.

### 7.5 Incoherencia concluyente

Si \(R_W\ne2\) y \(E_W=0\), no se fuerza una síntesis. \(A_i\) asciende solo, \(B_i\) ocupa la posición \(A\) de la ventana siguiente y entra el próximo tensor \(T_{i+1}\):

\[
(A_i,B_i,U_i)
\rightarrow
A_i^{\uparrow};
\qquad
W_{i+1}=(B_i,T_{i+1},U_0)
\]

### 7.6 Carry

Si \(R_W=2\), la relación permanece abierta. Pasa a la ventana siguiente el estado completo alcanzado por la consulta:

\[
\operatorname{Carry}_i=U_i^*
\]

\[
W_{i+1}=(U_i^*,T_{i+1},U_0)
\]

El carry incluye:

\[
U_i^*=
\bigl(
T_U^*,
SO_U,
DO_U,
DE_U,
DS_U,
\text{procedencia}
\bigr)
\]

No es solo C5, ni \(DE\), ni el par \((DE,DO)\). Tampoco es un tensor insertable en el diccionario por el mero hecho de existir como carry.

### 7.7 Frontera del clúster

Si no queda un nuevo tensor y la última relación entre \(A\) y \(B\) no es coherente, ninguno se descarta ni se obliga a cerrar. Ambos ascienden por separado y en orden al ciclo superior.

---

## 8. El diccionario

### 8.1 Función

El diccionario contiene tensores admitidos por el sistema y el conocimiento necesario para localizarlos y reejecutarlos. No es una memoria auxiliar pasiva: participa en cada búsqueda de \(U\).

Una entrada canónica conserva, como mínimo:

\[
\operatorname{Entry}(T)=
\bigl(
T,
DO_T,
DE_T,
DS_T,
\text{nivel},
\text{procedencia},
\text{traza de reejecución}
\bigr)
\]

### 8.2 Regla de admisión

Un tensor puede incorporarse al diccionario únicamente mediante un evento de entrada o admisión explícito:

\[
\operatorname{admit}(T)
\rightarrow
D\leftarrow D\cup\{T\}
\]

Esto incluye una unidad que entra desde el flujo, la red o un nivel inferior ya cerrado y que pasa a ser entrada efectiva de un nivel superior.

La consulta no equivale a admisión.

### 8.3 Búsqueda progresiva

La búsqueda comienza con:

\[
U_0=(2,2,\ldots,2)
\]

Cada SO local resuelve restricciones y consulta el conjunto compatible:

\[
\operatorname{query}(D,U_i)=D(U_i)
\]

La evolución posible es:

| Resultado de la consulta | Acción |
|---|---|
| una coincidencia congruente | recuperar y reutilizar la entrada existente |
| varias coincidencias | continuar resolviendo o conservar apertura |
| ninguna coincidencia y queda recorrido | reorientar la búsqueda sin escribir en \(D\) |
| ninguna coincidencia y recorrido agotado | marcar no resuelto; no crear una entrada |

### 8.4 Prohibición de creación por fallo

Queda excluida la regla:

\[
\text{fallo de búsqueda}
\not\Rightarrow
\text{nuevo tensor}
\]

Los estados \(U_1,U_2,\ldots,U^*\) son índices parciales y no candidatos almacenables. Si una coincidencia existe, se usa el tensor ya presente. Si no existe, la ventana conserva apertura, transporta carry o termina como no resuelta.

### 8.5 Competencia

La competencia ocurre entre entradas ya admitidas compatibles con el mismo índice parcial. La prioridad puede actualizarse por cierre y reutilización, pero una candidata fallida no debe borrarse globalmente: puede ser válida en otro contexto.

Verificar una candidata significa reejecutarla dentro de la relación actual.

---

## 9. Autosimilitud completa

La operación se repite en cuatro escalas:

| Escala | Tres elementos relacionados | Resultado |
|---|---|---|
| TriGate | \(A,B,M\) | \((R,E,O)\) |
| Cara | tripletas de \(A,B,U\) | \((DO,DE,DS)\) |
| Transcender | C4, C5 y C6 | \(SO_X\) y \((R^{\uparrow},E^{\uparrow},O^{\uparrow})\) |
| Ventana | \(SO_A,SO_B,SO_U\) | \(SO_W\) y decisión de propagación |

La secuencia común es:

\[
\boxed{
\text{ordenar}
\rightarrow
\text{relacionar}
\rightarrow
\text{proyectar}
\rightarrow
\text{reejecutar}
\rightarrow
\text{emerger o transportar}
}
\]

El punto decisivo es:

\[
\boxed{
\text{las SO locales construyen el estado}
}
\]

\[
\boxed{
\text{la SO de ventana decide su propagación}
}
\]

---

## 10. Ejecución distribuida

### 10.1 Red de autómatas relacionales

Cada TriGate conserva referencias a sus celdas. Cuando una celda cambia, solo se reactivan las relaciones que dependen de ella:

\[
\text{cambio}
\rightarrow
\text{TriGate}
\rightarrow
\text{cara}
\rightarrow
SO
\rightarrow
\text{relaciones dependientes}
\]

No existe un procesador central que traduzca resultados a instrucciones. La propagación de cambios produce la coordinación global.

### 10.2 Regla de actualización

Cada latido ejecuta:

1. leer una fotografía estable de las celdas y de \(DO_t\);
2. resolver las relaciones activadas en la dirección \(C\);
3. recalcular \((R,E_C,O)\);
4. formar \((DO_{t+1},DE,DS)\) con las procedencias canónicas;
5. publicar solo los paquetes modificados;
6. activar las relaciones dependientes en el latido siguiente.

La condición:

\[
\Delta SO=0
\quad\Longrightarrow\quad
\text{no emitir evento}
\]

concentra el coste en las regiones que todavía cambian.

### 10.3 DO como orden y gasto

Cada intento consume un estado no visitado de \(DO\). Para un \(DO\) de \(n\) trits, los estados admisibles siguen los números de Fibonacci no negativos, sin duplicados, codificados en base tres y limitados a \([0,3^n)\):

\[
0,1,2,3,5,8,13,\ldots
\]

Por ejemplo, para \(n=3\):

\[
000,001,002,010,012,022,111,\ldots
\]

La condición dura de parada es:

\[
\boxed{
\text{detener}
\iff
\nexists\ DO\ \text{admisible y no visitado}
}
\]

El contexto nuevo puede abrir un recorrido nuevo; sin cambio de contexto, un estado fallido no se repite.

### 10.4 Confluencia

TriGates independientes pueden ejecutarse en paralelo. Dos órdenes de eventos que parten de la misma fotografía deben:

- converger en el mismo cierre cuando representan la misma solución;
- o permanecer como ramas distintas cuando expresan soluciones legítimamente diferentes.

La reejecución sobre una fotografía estable debe reproducir el mismo resultado.

---

## 11. Algoritmo operativo de referencia

El siguiente pseudocódigo fija el orden de decisiones; no introduce operaciones ajenas al modelo.

```text
operar_ventana(A, B, diccionario, contexto):
    U <- abierto_con_misma_forma(A, B)
    visitados <- vacío

    repetir:
        foto <- snapshot(A, B, U, contexto, visitados)

        SO_A <- transcender(A, foto)
        SO_B <- transcender(B, foto)

        compatibles <- consultar(diccionario, U)
        SO_U <- transcender_busqueda(U, compatibles, foto)

        SO_W <- cara(SO_A, SO_B, SO_U, foto.DO)
        (R_W, E_W, O_W) <- proyectar(SO_W)

        si R_W == 2:
            devolver CARRY(U_completo)

        si E_W == 1:
            devolver EMERGER(unidad_ya_construida)

        si E_W == 0:
            devolver DESPLAZAR(A_solo, B)

        siguiente <- siguiente_DO_admisible(O_W, visitados)

        si no existe siguiente:
            devolver NO_RESUELTO(estado_completo)

        visitados <- visitados ∪ {siguiente}
        publicar_en_siguiente_latido(siguiente)
```

La función `consultar` es de solo lectura. Ninguna rama de `operar_ventana` inserta una entrada en el diccionario.

---

## 12. Reglas retiradas

Las siguientes reglas pertenecen a versiones anteriores y quedan explícitamente fuera del núcleo canónico:

1. **Decidir la ventana solo mediante \(DE\).** La decisión usa primero \(R_W\), después \(E_W\) y finalmente \(O_W\) y el gasto.
2. **Tratar C4, C5 y C6 como nivel de ventana.** Pertenecen al transcender.
3. **Permitir que un C4 local decida el carry global.** Solo \(SO_W\), formada con \(SO_A,SO_B,SO_U\), decide la propagación.
4. **Hacer nacer \(DO\) de los TriGates homólogos ES/FN/FO.** \(DO\) nace de los TriGates que ordenan \(P_A,P_B,P_U\).
5. **Usar la SO como traductor de señales externas.** Su propia operación modifica el estado compartido.
6. **Reducir el carry a C5, \(DE\) o \((DE,DO)\).** El carry es \(U^*\) completo.
7. **Interpretar \(U\) como tensor nuevo fabricado por la salida.** \(U\) es una búsqueda progresiva.
8. **Crear una tripleta o tensor cuando el diccionario no encuentra coincidencia.** Un fallo no escribe en el diccionario.
9. **Insertar automáticamente cada estado parcial de U.** Los estados parciales son índices transitorios.
10. **Aplicar distancias reales, Manhattan, puntuaciones o heurísticas externas para decidir cierre.** El núcleo decide por reejecución ternaria.
11. **Usar una regla excepcional de copia para inventar conocimiento vacío.** El conocimiento debe entrar por admisión y reutilizarse por consulta.
12. **Aplicar \(DO_{t+1}\) en el mismo intento que lo produce.** Toda actualización se difiere al latido siguiente.

---

## 13. Pruebas mínimas de conformidad

Una implementación no puede declararse conforme sin superar, como mínimo, estas pruebas.

### 13.1 TriGate

1. \(\operatorname{Maj}_3(0,0,1)=0\).
2. \(\operatorname{Maj}_3(1,0,1)=1\).
3. \(\operatorname{Maj}_3(0,1,2)=2\).
4. Para una permutación de \((2,2,1)\), si \(R=2\), entonces \(E=1\).
5. Para una permutación de \((2,2,0)\), si \(R=2\), entonces \(E=0\).
6. \((2,2,2)\) y una permutación de \((0,1,2)\) producen \((R,E)=(2,2)\), pero conservan distinta orientación o procedencia.

### 13.2 Ordenación y cara

7. \((0,1,2)\) no admite cierre literal por autorreferencia.
8. \(DO=(O_A,O_B,O_U)\) procede exclusivamente de los tres ordenadores.
9. \(DS\) se forma con \((R_{ES},R_{FN},R_{FO})\).
10. \(DE\) se forma con \((E_{ES},E_{FN},E_{FO})\).
11. Cambiar \(DO_{t+1}\) no altera el resultado ya publicado para \(t\).

### 13.3 Transcender y ventana

12. C4, C5 y C6 producen respectivamente los niveles \(R\), \(E\) y \(O\) del transcender.
13. Un C4 local igual a \(2\) no genera por sí solo el carry de ventana.
14. La ventana se decide a partir de \(SO_W=\Phi(SO_A,SO_B,SO_U)\).
15. Si \(R_W=2\), se transporta \(U^*\) completo.
16. Si \(R_W\ne2\) y \(E_W=1\), emerge la unidad ya construida.
17. Si \(R_W\ne2\) y \(E_W=0\), \(A\) asciende solo y \(B\) se desplaza.

### 13.4 Diccionario

18. Una coincidencia exacta reutiliza la misma identidad almacenada.
19. Una consulta ambigua no inserta una entrada.
20. Una consulta sin coincidencias no inserta una entrada.
21. Un carry no se incorpora al diccionario sin un evento posterior de admisión.

### 13.5 Ejecución

22. Un estado \(DO\) fallido no se repite mientras no cambie el contexto.
23. El agotamiento del recorrido detiene la búsqueda sin inventar un cierre.
24. La reejecución desde la misma fotografía produce el mismo paquete final.

---

## 14. Cierre arquitectónico

Aurora queda definido por una única pauta autosimilar:

\[
\text{relaciones locales}
\rightarrow
\text{construcción distribuida de }U^*
\rightarrow
SO_W
\rightarrow
\begin{cases}
\text{emergencia vertical}\\
\text{carry horizontal}\\
\text{desplazamiento incoherente}\\
\text{parada sin cierre}
\end{cases}
\]

La ventana no fabrica el tensor que transporta. El diccionario no inventa conocimiento al fallar. La semilla operativa no traduce resultados a comandos. Cada una de estas funciones emerge de relaciones ordinarias entre estructuras del mismo tipo.

La arquitectura está, por tanto, cerrada en sus niveles, tipos, procedencias y transiciones. El trabajo siguiente es empírico: implementar las tablas, ejecutar las pruebas de conformidad y medir convergencia, coste y capacidad de generalización.

---

## A. Nota sobre resultados anteriores

Las mediciones realizadas con prototipos previos —incluida la reducción de ventanas mediante lexicalización— constituyen evidencia exploratoria, no validación de esta especificación. Deben repetirse con:

- las dos familias canónicas de TriGates de cara;
- C4–C6 situadas en el transcender;
- la SO de ventana formada por \(SO_A,SO_B,SO_U\);
- \(U\) como consulta de solo lectura;
- la prohibición de crear tensores ante un fallo de búsqueda;
- el recorrido \(DO\) y las condiciones de parada aquí definidos.

---

## B. Licencias

El código de Aurora se distribuye bajo **Apache License 2.0**. La documentación se distribuye bajo **Creative Commons Attribution 4.0 (CC BY 4.0)**.

Las versiones modificadas o redistribuidas deben conservar los avisos de licencia correspondientes y atribuir claramente su procedencia al proyecto Aurora.ónica del núcleo relacional

**Versión:** 1.0  
**Fecha:** 9 de agosto de 2026  
**Estado:** arquitectura cerrada; referencia normativa para formalización, implementación y pruebas  
**Proyecto:** Aurora

---

## 0. Propósito y alcance

Aurora investiga una arquitectura de inteligencia artificial discreta, autosimilar y homoicónica. Su hipótesis es que datos, conocimiento, búsqueda, memoria y control pueden representarse mediante la misma clase de estructura ternaria y operarse con un único mecanismo relacional.

El objetivo no es construir un modelo probabilístico más pequeño, sino una máquina capaz de:

- aprender de forma local y continua;
- reutilizar conocimiento ya validado;
- buscar relaciones sin reconstruirlas estadísticamente en cada uso;
- compartir unidades de conocimiento verificables entre nodos;
- hacer emerger estructuras superiores mediante cierre;
- conservar como *carry* aquello que todavía necesita contexto.

Este documento define el núcleo canónico desde el TriGate hasta la ventana y el diccionario. Las explicaciones históricas, métricas de prototipos anteriores y variantes abandonadas no son normativas.

La jerarquía ejecutiva es:

\[
\boxed{
\text{TriGate}
\rightarrow
\text{cara}
\rightarrow
\text{transcender}
\rightarrow
\text{ventana}
\rightarrow
\text{diccionario}
}
\]

Cada nivel reutiliza la misma operación. Lo que cambia es el tipo de unidad que ocupa cada posición.

---

## 1. Vocabulario ternario e invariantes

### 1.1 Trit

Aurora usa el conjunto:

\[
\mathbb T=\{0,1,2\}
\]

- \(0\) y \(1\) son determinaciones complementarias.
- \(2\) representa apertura, indeterminación o valor todavía no resoluble en la relación actual.

En el orden parcial de información:

\[
2\sqsubseteq0,
\qquad
2\sqsubseteq1
\]

Resolver un \(2\) añade determinación. Mantenerlo conserva posibilidades.

### 1.2 Tripleta y tensor

Una tripleta es:

\[
P=(p_0,p_1,p_2),
\qquad p_i\in\mathbb T
\]

La construcción es recursiva:

\[
\mathcal T_0=\mathbb T,
\qquad
\mathcal T_{n+1}=\mathcal T_n^3
\]

Por tanto, un tensor Aurora no requiere otro operador: es una composición de tres unidades del nivel inferior.

### 1.3 Invariantes canónicas

Toda implementación debe conservar estas invariantes:

1. **Ternariedad:** el núcleo no introduce valores continuos para decidir cierre, búsqueda o control.
2. **Autosimilitud:** tres unidades del mismo nivel se operan mediante la misma forma relacional.
3. **Homoiconicidad:** una tripleta puede actuar como dato, conocimiento, índice, operación o control según su posición.
4. **Procedencia:** una unidad emergente conserva información suficiente para reordenarse y reejecutarse.
5. **Fotografía estable:** el estado producido en el intento \(t\) solo se aplica en \(t+1\).
6. **No creación durante la consulta:** una búsqueda fallida no inserta un tensor nuevo en el diccionario.
7. **Decisión local:** una SO modifica relaciones compartidas; no emite comandos externos a otro mecanismo.
8. **Propagación separada de construcción:** las SO locales construyen el estado; la ventana solo decide cómo se propaga.

---

## 2. El TriGate

### 2.1 Relación mínima

Un TriGate contiene:

\[
G=(A,B,M;R,E_C,O)
\]

donde:

| Símbolo | Papel |
|---|---|
| \(A\) | ancla de la relación |
| \(B\) | segundo operando |
| \(M\) | modo o función ternaria |
| \(R\) | resultado de la relación |
| \(E_C\) | estado relacional en la dirección \(C\) |
| \(O\) | orientación y siguiente recorrido |

El TriGate no debe interpretarse como una puerta de una sola dirección. Es una relación que puede recorrerse para resolver distintas posiciones.

### 2.2 Mayoría ternaria

La relación directa es:

\[
\widehat R=\operatorname{Maj}_3(A,B,M)
\]

con:

\[
\operatorname{Maj}_3(x,y,z)=
\begin{cases}
x,&x=y\ \lor\ x=z\\
y,&y=z\\
2,&x,y,z\ \text{son todos distintos}
\end{cases}
\]

Así, \(M=0\) se comporta como el sesgo conjuntivo, \(M=1\) como el sesgo disyuntivo y \(M=2\) conserva apertura cuando no aparece una mayoría determinada.

### 2.3 Dirección de resolución

La dirección \(C\) selecciona la celda transformable. \(A\) permanece como ancla.

| \(C\) | Celda resoluble | Operación |
|---:|---|---|
| \(0\) | \(B\) | deducción |
| \(1\) | \(R\) | inferencia |
| \(2\) | \(M\) | aprendizaje |

Inferir, deducir y aprender no son tres algoritmos. Son tres recorridos de la misma relación.

Para una dirección \(C\), el TriGate obtiene el conjunto de valores compatibles de la celda seleccionada:

\[
\mathcal S_C=
\{x\in\mathbb T:\operatorname{Maj}_3(A,B,M)=R\}
\]

sustituyendo por \(x\) la celda indicada por \(C\). Si existe más de una solución, \(O\) y el recorrido vigente determinan cuál se prueba; si todavía no puede elegirse una sin perder alternativas, la celda permanece en \(2\).

### 2.4 Emergencia \(E_C\)

\(E_C\) no es una votación adicional. Se recalcula después de operar en la dirección \(C\).

Sea:

\[
q=\operatorname{Maj}_3(A,B,M)
\]

Cuando \(R\in\{0,1\}\):

\[
E_C=
\begin{cases}
1,&q=R\\
0,&q\in\{0,1\}\ \land\ q\ne R\\
2,&q=2
\end{cases}
\]

Por tanto:

- \(E_C=1\): cierre coherente en la dirección ensayada;
- \(E_C=0\): contradicción o cierre complementario;
- \(E_C=2\): relación todavía abierta.

Cuando \(R=2\), \(E_C\) conserva el residual de la apertura:

| Configuración de \((A,B,M)\) | \(R\) | \(E_C\) |
|---|---:|---:|
| permutación de \((2,2,1)\) | \(2\) | \(1\) |
| permutación de \((2,2,0)\) | \(2\) | \(0\) |
| \((2,2,2)\) | \(2\) | \(2\) |
| permutación de \((0,1,2)\) | \(2\) | \(2\) |

Los dos últimos casos comparten \((R,E_C)=(2,2)\), pero no la misma procedencia. \(O\) los distingue.

### 2.5 Paquete observable

La salida completa del TriGate es:

\[
\operatorname{out}(G)=(R,E_C,O)
\]

Ninguno de sus componentes debe interpretarse aisladamente:

- \(R\) indica cierre o apertura del resultado;
- \(E_C\) califica ese estado o conserva su residual;
- \(O\) conserva desde dónde se leyó y cómo continuar.

---

## 3. Ordenación de una tripleta

### 3.1 Papeles ES, FN y FO

Ordenar no significa ordenar numéricamente. Significa asignar papeles relacionales:

- \(ES\): estructura;
- \(FN\): función;
- \(FO\): forma;
- \(O\): posición desde la que se lee la tripleta.

Para \(P=(p_0,p_1,p_2)\) y una orientación candidata \(o\):

\[
i_{ES}=o
\]

\[
ES=p_{i_{ES}}
\]

El valor de \(ES\) señala el índice de \(FN\):

\[
i_{FN}=ES
\]

La autorreferencia está prohibida:

\[
i_{FN}\ne i_{ES}
\]

El índice restante es \(i_{FO}\), y entonces:

\[
FN=p_{i_{FN}},
\qquad
FO=p_{i_{FO}}
\]

Una orientación es válida si no produce autorreferencia. Si existen varias, el estado vigente de \(DO\) selecciona la siguiente no visitada.

### 3.2 Tensor imposible y propósito abierto

En \((0,1,2)\), cada posición se señala a sí misma. Por ello, no existe una orientación literal válida:

\[
\operatorname{order}(0,1,2)=\varnothing
\]

La tripleta puede utilizarse como propósito abierto que mantiene la búsqueda orientada, pero no como cierre estructural literal.

### 3.3 Procedencia vertical

Cuando tres unidades forman otra superior:

\[
ES^{\uparrow}
=
ES_{\text{unidad inferior cuyo índice es }O^{\uparrow}}
\]

La orientación superior selecciona una relación inferior y conserva su estructura sin añadir un direccionador externo.

---

## 4. La cara

### 4.1 Entrada canónica

Una cara recibe tres tripletas del mismo nivel, procedentes de los tres tensores de la ventana:

\[
P_A,
\qquad
P_B,
\qquad
P_U
\]

\(A\) y \(B\) contienen contexto admitido. \(U\) es el tercer tensor abierto y comienza, en cada nueva ventana, con todos sus valores en \(2\):

\[
P_{U,0}=(2,2,2)
\]

La tercera tripleta no es un tercer token observado. Es la porción local de la búsqueda que todavía debe resolverse.

### 4.2 Dos familias entrelazadas de TriGates

La cara contiene dos familias con procedencias distintas.

#### A. TriGates de ordenación

Cada tripleta se ordena independientemente:

\[
Q_X(P_X)=(ES_X,FN_X,FO_X,O_X),
\qquad
X\in\{A,B,U\}
\]

Sus orientaciones forman:

\[
\boxed{DO=(O_A,O_B,O_U)}
\]

\(DO\) conserva cómo fueron leídos los tres tensores.

#### B. TriGates relacionales

Después de ordenar, se operan las coordenadas homólogas:

\[
G_{ES}=(ES_A,ES_B,ES_U)
\]

\[
G_{FN}=(FN_A,FN_B,FN_U)
\]

\[
G_{FO}=(FO_A,FO_B,FO_U)
\]

Cada grupo produce \((R,E_C,O)\), pero la cara proyecta canónicamente:

\[
\boxed{DS=(R_{ES},R_{FN},R_{FO})}
\]

\[
\boxed{DE_C=(E_{ES,C},E_{FN,C},E_{FO,C})}
\]

La procedencia normativa es, por tanto:

\[
\boxed{
\text{ordenación}\rightarrow DO
\qquad
\text{relación}\rightarrow(DE,DS)
}
\]

Los \(O\) internos de \(G_{ES}\), \(G_{FN}\) y \(G_{FO}\) pueden orientar la reejecución de esos TriGates, pero no sustituyen el \(DO\) canónico de la cara.

### 4.3 Conocimiento de cara

La salida completa se escribe en orden operativo:

\[
K=(DO,DE,DS)
\]

| Canal | Procedencia | Significado |
|---|---|---|
| \(DO\) | orientaciones de \(P_A,P_B,P_U\) | orden y recorrido |
| \(DE\) | emergencias de \(G_{ES},G_{FN},G_{FO}\) | estado relacional |
| \(DS\) | resultados de \(G_{ES},G_{FN},G_{FO}\) | síntesis local |

\(K\) no es un registro externo. Es otra tripleta Aurora. Puede ordenarse y entrar en una cara superior, donde producirá su propio \(DS^{\uparrow}\).

### 4.4 Fotografía estable

La cara lee \(DO_t\), ejecuta el intento y publica \(DO_{t+1}\):

\[
DO_t
\rightarrow
\operatorname{cara}_t
\rightarrow
DO_{t+1}
\]

\(DO_{t+1}\) nunca modifica retrospectivamente el intento que lo produjo.

---

## 5. Semilla operativa y evolución de U

### 5.1 La semilla operativa

Una semilla operativa, \(SO\), es una relación Aurora ordinaria que reúne el estado producido por las caras conectadas. No interpreta sus salidas para generar órdenes externas.

Su operación cambia celdas compartidas:

\[
\operatorname{SO}
\rightarrow
\text{nuevo estado relacional}
\rightarrow
\text{reactivación de las relaciones dependientes}
\]

El control es, por ello, información operada mediante el mismo mecanismo que los datos.

### 5.2 Tres representaciones del mismo desconocido

En la rama de salida deben identificarse como aspectos de un mismo proceso:

1. la tercera tripleta local \(P_U\);
2. la SO de salida \(SO_U\);
3. el tensor abierto \(U\) de la ventana.

No son tres objetos de conocimiento independientes. Son tres escalas de la misma consulta mientras se determina:

\[
U_0
\rightarrow
U_1
\rightarrow
\cdots
\rightarrow
U^*
\]

Cada actualización local añade restricciones a la búsqueda. No acuña un tensor.

### 5.3 Interpretación como índice parcial

Sea \(D\) el diccionario y \(D(U_i)\) el conjunto de entradas compatibles con el estado parcial de \(U_i\). La resolución progresa idealmente como:

\[
D(U_0)
\supseteq
D(U_1)
\supseteq
\cdots
\supseteq
D(U^*)
\]

Un paso puede mantener el conjunto si todavía no añade información, pero no debe ampliarlo sin que cambie el contexto o se retroceda explícitamente a otra rama.

---

## 6. El transcender

### 6.1 Escala de entrada, conocimiento y salida

El transcender relaciona tres unidades del mismo tipo:

\[
I=\text{entrada},
\qquad
K=\text{conocimiento},
\qquad
S=\text{salida}
\]

Cada unidad conserva:

- su tripleta ordenable \((ES,FN,FO)\);
- su conocimiento asociado \((DO,DE,DS)\).

La salida comienza abierta cuando todavía no existe una coincidencia seleccionada:

\[
S_0=(2,2,2)
\]

### 6.2 Caras C4, C5 y C6

C4, C5 y C6 pertenecen al transcender, no a la ventana.

| Cara | Canales relacionados | Proyección superior | Papel |
|---|---|---|---|
| C4 | \((DS_I,DS_K,DS_S)\) | \(R^{\uparrow}\) | resultado |
| C5 | \((DE_I,DE_K,DE_S)\) | \(E^{\uparrow}\) | coherencia o residual |
| C6 | \((DO_I,DO_K,DO_S)\) | \(O^{\uparrow}\) | orden y continuación |

En forma compacta:

\[
\boxed{
C4\equiv R^{\uparrow},
\qquad
C5\equiv E^{\uparrow},
\qquad
C6\equiv O^{\uparrow}
}
\]

Sus tres estados se relacionan mediante la misma operación y forman la semilla operativa del transcender:

\[
SO_X=\Phi(C4_X,C5_X,C6_X)
\]

### 6.3 Lectura jerárquica de C4 y C5

Primero se interpreta C4.

Si:

\[
R^{\uparrow}=2
\]

la relación del transcender sigue abierta. C5 conserva entonces el residual que participa en el carry local:

\[
C4=2
\quad\Longrightarrow\quad
C5=\text{estado relacional pendiente}
\]

Si:

\[
R^{\uparrow}\in\{0,1\}
\]

C5 recupera su función de evaluación:

\[
C4\ne2
\quad\Longrightarrow\quad
C5=\text{coherencia del cierre}
\]

C6 conserva la orientación desde la que se obtuvo cualquiera de los dos estados.

### 6.4 Límite de la decisión local

Una apertura en C4 de un solo transcender no decide por sí misma el movimiento de toda la ventana. Solo queda incorporada a \(SO_X\). La decisión global se produce un nivel después.

---

## 7. La ventana

### 7.1 Composición

La ventana opera tres tensores del mismo nivel:

\[
W_i=(A_i,B_i,U_i)
\]

- \(A_i\) y \(B_i\) proceden del clúster tensorial o de la propagación anterior.
- \(U_i\) es la consulta abierta, con la misma forma y nivel que \(A_i\) y \(B_i\).
- Al abrir una ventana nueva:

\[
U_0=(2,2,\ldots,2)
\]

Cada tensor posee su transcender y su SO:

\[
SO_A,
\qquad
SO_B,
\qquad
SO_U
\]

### 7.2 Semilla operativa de ventana

La ventana no se decide directamente mediante C4, C5 y C6. Relaciona las tres semillas ya construidas:

\[
\boxed{
SO_W=\Phi(SO_A,SO_B,SO_U)
}
\]

La proyección superior de \(SO_W\) produce:

\[
(R_W,E_W,O_W)
\]

Este paquete decide únicamente la propagación del estado inferior. No vuelve a construirlo.

### 7.3 Tabla canónica de transición

La lectura es jerárquica: primero \(R_W\); si ha cerrado, \(E_W\); \(O_W\) orienta el siguiente intento.

| \(R_W\) | \(E_W\) | Condición adicional | Acción de la ventana |
|---:|---:|---|---|
| \(2\) | cualquiera | relación abierta | transportar \(U_i^*\) completo como carry |
| \(0\) o \(1\) | \(1\) | cierre congruente | emerger verticalmente la unidad ya construida |
| \(0\) o \(1\) | \(0\) | incoherencia concluyente | no sintetizar \(A_i\) con \(B_i\); desplazar la ventana |
| \(0\) o \(1\) | \(2\) | queda \(DO\) admisible | continuar en la orientación \(O_W\) |
| cualquiera | cualquiera | recorrido agotado y ninguna decisión anterior | conservar el estado y marcar no resuelto |

La prioridad semántica es:

\[
\boxed{
R_W
\rightarrow
E_W
\rightarrow
O_W
\rightarrow
\text{gasto}
}
\]

El agotamiento se consulta únicamente cuando el paquete todavía exige otro intento. Un cierre, una incoherencia concluyente o un carry ya determinados no se revierten por haber consumido el último estado del recorrido.

### 7.4 Emergencia coherente

Si \(R_W\ne2\) y \(E_W=1\), la ventana reconoce que la estructura construida por las SO locales puede ascender:

\[
W_i
\rightarrow
T_i^{\uparrow}
\]

\(T_i^{\uparrow}\) conserva la procedencia de \(A_i\), \(B_i\), la coincidencia recuperada para \(U_i\) y sus paquetes \((DO,DE,DS)\).

La ventana no calcula de nuevo \(T_i^{\uparrow}\). Solo habilita su movimiento vertical.

### 7.5 Incoherencia concluyente

Si \(R_W\ne2\) y \(E_W=0\), no se fuerza una síntesis. \(A_i\) asciende solo, \(B_i\) ocupa la posición \(A\) de la ventana siguiente y entra el próximo tensor \(T_{i+1}\):

\[
(A_i,B_i,U_i)
\rightarrow
A_i^{\uparrow};
\qquad
W_{i+1}=(B_i,T_{i+1},U_0)
\]

### 7.6 Carry

Si \(R_W=2\), la relación permanece abierta. Pasa a la ventana siguiente el estado completo alcanzado por la consulta:

\[
\operatorname{Carry}_i=U_i^*
\]

\[
W_{i+1}=(U_i^*,T_{i+1},U_0)
\]

El carry incluye:

\[
U_i^*=
\bigl(
T_U^*,
SO_U,
DO_U,
DE_U,
DS_U,
\text{procedencia}
\bigr)
\]

No es solo C5, ni \(DE\), ni el par \((DE,DO)\). Tampoco es un tensor insertable en el diccionario por el mero hecho de existir como carry.

### 7.7 Frontera del clúster

Si no queda un nuevo tensor y la última relación entre \(A\) y \(B\) no es coherente, ninguno se descarta ni se obliga a cerrar. Ambos ascienden por separado y en orden al ciclo superior.

---

## 8. El diccionario

### 8.1 Función

El diccionario contiene tensores admitidos por el sistema y el conocimiento necesario para localizarlos y reejecutarlos. No es una memoria auxiliar pasiva: participa en cada búsqueda de \(U\).

Una entrada canónica conserva, como mínimo:

\[
\operatorname{Entry}(T)=
\bigl(
T,
DO_T,
DE_T,
DS_T,
\text{nivel},
\text{procedencia},
\text{traza de reejecución}
\bigr)
\]

### 8.2 Regla de admisión

Un tensor puede incorporarse al diccionario únicamente mediante un evento de entrada o admisión explícito:

\[
\operatorname{admit}(T)
\rightarrow
D\leftarrow D\cup\{T\}
\]

Esto incluye una unidad que entra desde el flujo, la red o un nivel inferior ya cerrado y que pasa a ser entrada efectiva de un nivel superior.

La consulta no equivale a admisión.

### 8.3 Búsqueda progresiva

La búsqueda comienza con:

\[
U_0=(2,2,\ldots,2)
\]

Cada SO local resuelve restricciones y consulta el conjunto compatible:

\[
\operatorname{query}(D,U_i)=D(U_i)
\]

La evolución posible es:

| Resultado de la consulta | Acción |
|---|---|
| una coincidencia congruente | recuperar y reutilizar la entrada existente |
| varias coincidencias | continuar resolviendo o conservar apertura |
| ninguna coincidencia y queda recorrido | reorientar la búsqueda sin escribir en \(D\) |
| ninguna coincidencia y recorrido agotado | marcar no resuelto; no crear una entrada |

### 8.4 Prohibición de creación por fallo

Queda excluida la regla:

\[
\text{fallo de búsqueda}
\not\Rightarrow
\text{nuevo tensor}
\]

Los estados \(U_1,U_2,\ldots,U^*\) son índices parciales y no candidatos almacenables. Si una coincidencia existe, se usa el tensor ya presente. Si no existe, la ventana conserva apertura, transporta carry o termina como no resuelta.

### 8.5 Competencia

La competencia ocurre entre entradas ya admitidas compatibles con el mismo índice parcial. La prioridad puede actualizarse por cierre y reutilización, pero una candidata fallida no debe borrarse globalmente: puede ser válida en otro contexto.

Verificar una candidata significa reejecutarla dentro de la relación actual.

---

## 9. Autosimilitud completa

La operación se repite en cuatro escalas:

| Escala | Tres elementos relacionados | Resultado |
|---|---|---|
| TriGate | \(A,B,M\) | \((R,E,O)\) |
| Cara | tripletas de \(A,B,U\) | \((DO,DE,DS)\) |
| Transcender | C4, C5 y C6 | \(SO_X\) y \((R^{\uparrow},E^{\uparrow},O^{\uparrow})\) |
| Ventana | \(SO_A,SO_B,SO_U\) | \(SO_W\) y decisión de propagación |

La secuencia común es:

\[
\boxed{
\text{ordenar}
\rightarrow
\text{relacionar}
\rightarrow
\text{proyectar}
\rightarrow
\text{reejecutar}
\rightarrow
\text{emerger o transportar}
}
\]

El punto decisivo es:

\[
\boxed{
\text{las SO locales construyen el estado}
}
\]

\[
\boxed{
\text{la SO de ventana decide su propagación}
}
\]

---

## 10. Ejecución distribuida

### 10.1 Red de autómatas relacionales

Cada TriGate conserva referencias a sus celdas. Cuando una celda cambia, solo se reactivan las relaciones que dependen de ella:

\[
\text{cambio}
\rightarrow
\text{TriGate}
\rightarrow
\text{cara}
\rightarrow
SO
\rightarrow
\text{relaciones dependientes}
\]

No existe un procesador central que traduzca resultados a instrucciones. La propagación de cambios produce la coordinación global.

### 10.2 Regla de actualización

Cada latido ejecuta:

1. leer una fotografía estable de las celdas y de \(DO_t\);
2. resolver las relaciones activadas en la dirección \(C\);
3. recalcular \((R,E_C,O)\);
4. formar \((DO_{t+1},DE,DS)\) con las procedencias canónicas;
5. publicar solo los paquetes modificados;
6. activar las relaciones dependientes en el latido siguiente.

La condición:

\[
\Delta SO=0
\quad\Longrightarrow\quad
\text{no emitir evento}
\]

concentra el coste en las regiones que todavía cambian.

### 10.3 DO como orden y gasto

Cada intento consume un estado no visitado de \(DO\). Para un \(DO\) de \(n\) trits, los estados admisibles siguen los números de Fibonacci no negativos, sin duplicados, codificados en base tres y limitados a \([0,3^n)\):

\[
0,1,2,3,5,8,13,\ldots
\]

Por ejemplo, para \(n=3\):

\[
000,001,002,010,012,022,111,\ldots
\]

La condición dura de parada es:

\[
\boxed{
\text{detener}
\iff
\nexists\ DO\ \text{admisible y no visitado}
}
\]

El contexto nuevo puede abrir un recorrido nuevo; sin cambio de contexto, un estado fallido no se repite.

### 10.4 Confluencia

TriGates independientes pueden ejecutarse en paralelo. Dos órdenes de eventos que parten de la misma fotografía deben:

- converger en el mismo cierre cuando representan la misma solución;
- o permanecer como ramas distintas cuando expresan soluciones legítimamente diferentes.

La reejecución sobre una fotografía estable debe reproducir el mismo resultado.

---

## 11. Algoritmo operativo de referencia

El siguiente pseudocódigo fija el orden de decisiones; no introduce operaciones ajenas al modelo.

```text
operar_ventana(A, B, diccionario, contexto):
    U <- abierto_con_misma_forma(A, B)
    visitados <- vacío

    repetir:
        foto <- snapshot(A, B, U, contexto, visitados)

        SO_A <- transcender(A, foto)
        SO_B <- transcender(B, foto)

        compatibles <- consultar(diccionario, U)
        SO_U <- transcender_busqueda(U, compatibles, foto)

        SO_W <- cara(SO_A, SO_B, SO_U, foto.DO)
        (R_W, E_W, O_W) <- proyectar(SO_W)

        si R_W == 2:
            devolver CARRY(U_completo)

        si E_W == 1:
            devolver EMERGER(unidad_ya_construida)

        si E_W == 0:
            devolver DESPLAZAR(A_solo, B)

        siguiente <- siguiente_DO_admisible(O_W, visitados)

        si no existe siguiente:
            devolver NO_RESUELTO(estado_completo)

        visitados <- visitados ∪ {siguiente}
        publicar_en_siguiente_latido(siguiente)
```

La función `consultar` es de solo lectura. Ninguna rama de `operar_ventana` inserta una entrada en el diccionario.

---

## 12. Reglas retiradas

Las siguientes reglas pertenecen a versiones anteriores y quedan explícitamente fuera del núcleo canónico:

1. **Decidir la ventana solo mediante \(DE\).** La decisión usa primero \(R_W\), después \(E_W\) y finalmente \(O_W\) y el gasto.
2. **Tratar C4, C5 y C6 como nivel de ventana.** Pertenecen al transcender.
3. **Permitir que un C4 local decida el carry global.** Solo \(SO_W\), formada con \(SO_A,SO_B,SO_U\), decide la propagación.
4. **Hacer nacer \(DO\) de los TriGates homólogos ES/FN/FO.** \(DO\) nace de los TriGates que ordenan \(P_A,P_B,P_U\).
5. **Usar la SO como traductor de señales externas.** Su propia operación modifica el estado compartido.
6. **Reducir el carry a C5, \(DE\) o \((DE,DO)\).** El carry es \(U^*\) completo.
7. **Interpretar \(U\) como tensor nuevo fabricado por la salida.** \(U\) es una búsqueda progresiva.
8. **Crear una tripleta o tensor cuando el diccionario no encuentra coincidencia.** Un fallo no escribe en el diccionario.
9. **Insertar automáticamente cada estado parcial de U.** Los estados parciales son índices transitorios.
10. **Aplicar distancias reales, Manhattan, puntuaciones o heurísticas externas para decidir cierre.** El núcleo decide por reejecución ternaria.
11. **Usar una regla excepcional de copia para inventar conocimiento vacío.** El conocimiento debe entrar por admisión y reutilizarse por consulta.
12. **Aplicar \(DO_{t+1}\) en el mismo intento que lo produce.** Toda actualización se difiere al latido siguiente.

---

## 13. Pruebas mínimas de conformidad

Una implementación no puede declararse conforme sin superar, como mínimo, estas pruebas.

### 13.1 TriGate

1. \(\operatorname{Maj}_3(0,0,1)=0\).
2. \(\operatorname{Maj}_3(1,0,1)=1\).
3. \(\operatorname{Maj}_3(0,1,2)=2\).
4. Para una permutación de \((2,2,1)\), si \(R=2\), entonces \(E=1\).
5. Para una permutación de \((2,2,0)\), si \(R=2\), entonces \(E=0\).
6. \((2,2,2)\) y una permutación de \((0,1,2)\) producen \((R,E)=(2,2)\), pero conservan distinta orientación o procedencia.

### 13.2 Ordenación y cara

7. \((0,1,2)\) no admite cierre literal por autorreferencia.
8. \(DO=(O_A,O_B,O_U)\) procede exclusivamente de los tres ordenadores.
9. \(DS\) se forma con \((R_{ES},R_{FN},R_{FO})\).
10. \(DE\) se forma con \((E_{ES},E_{FN},E_{FO})\).
11. Cambiar \(DO_{t+1}\) no altera el resultado ya publicado para \(t\).

### 13.3 Transcender y ventana

12. C4, C5 y C6 producen respectivamente los niveles \(R\), \(E\) y \(O\) del transcender.
13. Un C4 local igual a \(2\) no genera por sí solo el carry de ventana.
14. La ventana se decide a partir de \(SO_W=\Phi(SO_A,SO_B,SO_U)\).
15. Si \(R_W=2\), se transporta \(U^*\) completo.
16. Si \(R_W\ne2\) y \(E_W=1\), emerge la unidad ya construida.
17. Si \(R_W\ne2\) y \(E_W=0\), \(A\) asciende solo y \(B\) se desplaza.

### 13.4 Diccionario

18. Una coincidencia exacta reutiliza la misma identidad almacenada.
19. Una consulta ambigua no inserta una entrada.
20. Una consulta sin coincidencias no inserta una entrada.
21. Un carry no se incorpora al diccionario sin un evento posterior de admisión.

### 13.5 Ejecución

22. Un estado \(DO\) fallido no se repite mientras no cambie el contexto.
23. El agotamiento del recorrido detiene la búsqueda sin inventar un cierre.
24. La reejecución desde la misma fotografía produce el mismo paquete final.

---

## 14. Cierre arquitectónico

Aurora queda definido por una única pauta autosimilar:

\[
\text{relaciones locales}
\rightarrow
\text{construcción distribuida de }U^*
\rightarrow
SO_W
\rightarrow
\begin{cases}
\text{emergencia vertical}\\
\text{carry horizontal}\\
\text{desplazamiento incoherente}\\
\text{parada sin cierre}
\end{cases}
\]

La ventana no fabrica el tensor que transporta. El diccionario no inventa conocimiento al fallar. La semilla operativa no traduce resultados a comandos. Cada una de estas funciones emerge de relaciones ordinarias entre estructuras del mismo tipo.

La arquitectura está, por tanto, cerrada en sus niveles, tipos, procedencias y transiciones. El trabajo siguiente es empírico: implementar las tablas, ejecutar las pruebas de conformidad y medir convergencia, coste y capacidad de generalización.

---

## A. Nota sobre resultados anteriores

Las mediciones realizadas con prototipos previos —incluida la reducción de ventanas mediante lexicalización— constituyen evidencia exploratoria, no validación de esta especificación. Deben repetirse con:

- las dos familias canónicas de TriGates de cara;
- C4–C6 situadas en el transcender;
- la SO de ventana formada por \(SO_A,SO_B,SO_U\);
- \(U\) como consulta de solo lectura;
- la prohibición de crear tensores ante un fallo de búsqueda;
- el recorrido \(DO\) y las condiciones de parada aquí definidos.

---

## B. Licencias

El código de Aurora se distribuye bajo **Apache License 2.0**. La documentación se distribuye bajo **Creative Commons Attribution 4.0 (CC BY 4.0)**.

Las versiones modificadas o redistribuidas deben conservar los avisos de licencia correspondientes y atribuir claramente su procedencia al proyecto Aurora.


