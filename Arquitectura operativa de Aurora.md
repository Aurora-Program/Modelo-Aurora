# Arquitectura operativa de Aurora

## 1. Trits

Aurora opera con valores ternarios o **trits**:

[
{0,1,2}
]

donde:

* (0): desactivado, nulo, falso o apagado.
* (1): activado, existente, verdadero o encendido.
* (2): desconocido, abierto, fuera del espacio determinado o situado más allá del espacio actualmente representado.

El valor (2) no expresa una simple ausencia de información. Representa un espacio abierto que el sistema puede intentar resolver mediante sus relaciones y el conocimiento almacenado.

---

## 2. Tripleta

Una **tripleta** está formada por tres trits:

[
(x_0,x_1,x_2)
]

Por ejemplo:

[
(1,2,1)
]

Una vez ordenada, cada posición adquiere uno de los siguientes roles:

[
(FO,ES,FN)
]

donde:

* (ES): estructura u orientación.
* (FN): función o relación.
* (FO): forma o valor restante.
* (O): orden u orientación de lectura de la tripleta.

Por ejemplo:

[
O=1,\qquad (1,2,1)\longrightarrow(FO,ES,FN)
]

El valor de (ES) determina el índice de (FN), mientras que (FO) corresponde al valor restante. De este modo, la tripleta no representa únicamente tres valores, sino una estructura relacional ordenada.

---

## 3. Semilla Operativa

Una **Semilla Operativa**, o (SO), es una estructura fractal formada por tripletas organizadas recursivamente.

Ejemplo:

[
N_1:(1,1,1)
]

[
N_2:(0,2,1),;(0,0,1),;(1,2,1)
]

El nivel (N_2) puede interpretarse simultáneamente como:

* el segundo nivel de una semilla (SO_1);
* el primer nivel de tres semillas subordinadas: (SO_2), (SO_3) y (SO_4).

Por tanto, una misma estructura puede actuar como resultado de un nivel inferior y como entrada del nivel inmediatamente superior.

---

## 4. Tensor fractal

Un **tensor**, representado por (t), es una composición recursiva de Semillas Operativas.

Ejemplo:

[
N_1:(1,1,1)
]

[
N_2:(0,2,1),;(0,0,1),;(1,2,1)
]

[
N_3:
\begin{aligned}
&[(0,2,1),(0,0,1),(1,2,1)],\
&[(0,2,1),(0,0,1),(1,2,1)],\
&[(0,2,1),(0,0,1),(1,2,1)]
\end{aligned}
]

La estructura sigue una progresión fractal:

[
1\rightarrow3\rightarrow9\rightarrow27\rightarrow\cdots
]

Cada nivel sintetiza tres estructuras del nivel anterior y, al mismo tiempo, constituye una nueva unidad operativa para el nivel siguiente.

El tensor que asciende debe conservar su estructura completa:

[
T=(DS,DE,DO,\Pi)
]

donde:

* (DS): dimensión superior o síntesis estructural.
* (DE): dimensión de coherencia.
* (DO): dimensión de ordenación.
* (\Pi): procedencia o composición del tensor.

---

## 5. Clúster tensorial

Un **clúster** es una secuencia ordenada de tensores:

[
t_1,t_2,t_3,t_4,t_5,\ldots
]

Los tensores del clúster son evaluados mediante ventanas sucesivas. Cada ventana determina qué estructura asciende al ciclo superior y qué información debe continuar en la siguiente evaluación.

---

## 6. Ventana tensorial

Una ventana (W) contiene tres tensores:

[
W=[T_1,T_2,U]
]

donde:

* (T_1): primer tensor de entrada.
* (T_2): segundo tensor de entrada.
* (U): tensor abierto o desconocido, inicialmente compuesto por valores (2).

El tensor (U) representa la capa de conocimiento que la ventana intenta recuperar o reconstruir mediante el diccionario.

La operación de la ventana genera:

* (T_E): tensor emergente.
* (T_S): tensor de salida recuperado del diccionario.

El tensor (T_S) debe corresponder a un tensor que haya entrado previamente en el sistema y haya sido almacenado en el diccionario. El diccionario no crea conocimiento arbitrario: recupera, contrasta y reorganiza estructuras previamente observadas o calculadas.

### 6.1. Estados de la ventana

La coherencia de la ventana se representa mediante:

[
DE=
\begin{cases}
0 & \text{coherente}\
1 & \text{incoherente}\
2 & \text{ambigua}
\end{cases}
]

### Ventana coherente

Si la ventana es coherente, el tensor emergente (T_E) asciende al nivel o ciclo superior.

La ventana se desplaza hacia los siguientes tensores del clúster:

[
[T_1,T_2,U]\longrightarrow[T_3,T_4,U']
]

### Ventana incoherente

Si la ventana es incoherente, (T_1) asciende individualmente al nivel superior.

El segundo tensor pasa a ocupar la primera posición de la ventana siguiente:

[
[T_1,T_2,U]\longrightarrow[T_2,T_3,U']
]

De esta manera, la incoherencia no destruye los tensores ni fuerza una síntesis falsa. Se conserva el orden y se intenta una nueva relación.

### Ventana ambigua

Si la ventana permanece abierta o ambigua, la evolución del tensor desconocido produce un tensor emergente (T_E), que continúa como **carry**:

[
[T_1,T_2,U]\longrightarrow[T_E,T_3,U']
]

El carry transporta el conocimiento parcial obtenido en la ventana anterior sin declararlo todavía coherente.

### Última ventana

La última ventana debe completar el recorrido del clúster.

* Si es coherente, asciende (T_E).
* Si es incoherente, los tensores restantes ascienden por separado y conservan su orden.
* Si es ambigua, (T_E) asciende como carry abierto y no como síntesis consolidada.

También puede incorporarse un tensor terminal (0) para efectuar un último cierre explícito:

[
[T_E,T_{\text{final}},0]
]

De este modo, el final del clúster no convierte automáticamente una relación ambigua en coherente.

---

# 7. TriGate

El **TriGate** es la unidad relacional elemental de Aurora.

Todas sus entradas y salidas operan mediante trits. Está formado por:

* dos valores de entrada: (A) y (B);
* un modo lógico: (M);
* un resultado: (R);
* un estado relacional: (E);
* una orientación operativa: (C);
* una orientación posterior: (O).

Su forma general es:

[
T(A,B,M;R,E,C,O)
]

## 7.1. Modos lógicos

El valor (M) selecciona una función lógica ternaria:

[
M=
\begin{cases}
0 & AND3\
1 & OR3\
2 & UNKNOWN3
\end{cases}
]

El TriGate devuelve un resultado determinado cuando las operaciones (AND3) y (OR3) convergen para las entradas recibidas.

Por ejemplo:

[
0,0\longrightarrow0
]

[
1,1\longrightarrow1
]

Bajo estas condiciones, el TriGate se comporta como una función ternaria de mayoría. Sin embargo, su finalidad no es únicamente calcular un valor, sino evaluar y reconstruir una relación.

---

## 7.2. Resultado y estado relacional

Cuando (R\in{0,1}), (E) evalúa la coherencia de la relación entre (A), (B), (M) y (R):

[
E=
\begin{cases}
0 & \text{mayoría coherente con }R\
1 & \text{antimayoría o resultado opuesto a }R\
2 & \text{relación todavía ambigua}
\end{cases}
]

La antimayoría invierte los valores determinados:

[
0\longleftrightarrow1
]

mientras que:

[
2\longrightarrow2
]

Por tanto:

* con (R\in{0,1}), (E=0) produce activación o confirmación;
* (E=1) produce desactivación, contradicción o inversión;
* (E=2) indica que la relación permanece abierta.

### Cambio de función cuando (R=2)

Cuando (R=2), no existe todavía un resultado determinado que pueda evaluarse. En ese caso, (E) cambia de función y conserva el valor residual de la relación:

[
R=2\Longrightarrow E=\operatorname{residuo}(A,B,M)
]

Por ejemplo:

[
(2,2,1;R=2)\longrightarrow E=1
]

[
(2,2,0;R=2)\longrightarrow E=0
]

[
(2,2,2;R=2)\longrightarrow E=2
]

En este contexto, (E) actúa como una forma de retroprogramación: orienta el valor abierto hacia la solución más próxima compatible con la relación.

Existe así una analogía con una neurona, aunque el TriGate es más complejo:

* (R) se aproxima a una salida o activación;
* (E) se aproxima a una señal discreta de coherencia o corrección;
* (R=2) representa ambigüedad;
* (E\in{0,1,2}) funciona como un gradiente relacional ternario.

No se trata de un gradiente estadístico, sino de una orientación lógica discreta.

---

## 7.3. TriGate como autómata

El valor (2) actúa como orientador del proceso.

Si el TriGate contiene un único valor abierto, puede intentar resolver cualquiera de sus componentes:

[
A,;B,;M,;R
]

El control (C) determina la operación que debe realizar:

[
C=
\begin{cases}
0 & \text{deducción: reconstruir una entrada}\
1 & \text{inferencia: calcular }R\
2 & \text{aprendizaje: calcular }M
\end{cases}
]

Cuando (C=0), la posición del valor abierto permite distinguir si debe reconstruirse (A) o (B).

El ciclo del autómata es:

1. Detectar el valor (2).
2. Determinar mediante (C) qué operación corresponde.
3. Buscar los valores compatibles con la relación.
4. Sustituir el (2) si existe una solución determinada.
5. Mantener (2) si existen varias soluciones posibles.
6. Detenerse cuando no quedan valores abiertos o cuando la ambigüedad no puede resolverse.

Así:

* si no queda ningún (2), el TriGate ha alcanzado un cierre local;
* si queda una única solución, el valor se propaga;
* si existen varias soluciones, el TriGate permanece ambiguo;
* si no existe ninguna solución válida, la relación queda incoherente.

De esta forma, el TriGate puede entenderse como un autómata relacional con capacidad de decisión local.

---

## 7.4. Valores compartidos y propagación

Los TriGates no operan necesariamente sobre copias independientes de los datos, sino sobre valores compartidos mediante referencias o punteros.

Cuando un TriGate modifica un valor, el cambio desencadena un evento en todos los TriGates que comparten ese dato. Cada uno vuelve entonces a evaluar su relación e intenta resolver los valores (2) que hayan quedado a su alcance.

La coordinación global no depende de un controlador central. Surge de:

* las decisiones locales;
* los valores compartidos;
* la propagación de eventos;
* la redundancia de las relaciones;
* el cierre progresivo de los espacios abiertos.

---

# 8. Ordenación de las tripletas

La primera estructura compleja de Aurora es la tripleta:

[
(x_0,x_1,x_2)
]

Sus tres valores adoptan los roles:

[
ES,;FN,;FO
]

El valor de (ES) determina el índice ocupado por (FN). El valor restante adopta el papel de (FO).

Inicialmente, (FN) puede contener el valor (2), pues representa la función o relación que debe descubrirse.

En la ordenación:

* (R) representa (ES);
* (FN) ocupa la posición indicada por (ES);
* (FO) queda determinado por exclusión;
* (E) evalúa la relación;
* (O) registra la orientación resultante.

Ejemplos:

### Ejemplo 1

[
(1,2,1)
]

El valor abierto ocupa la posición correspondiente a (FN), por lo que:

[
R=ES=1
]

La relación ((1,1,2)) es coherente con (R=1):

[
E=0,\qquad O=0
]

### Ejemplo 2

[
(0,2,1)
]

De nuevo:

[
R=ES=1
]

La relación ((0,1,2)) no puede cerrarse de forma determinada:

[
E=2,\qquad O=2
]

### Ejemplo 3

[
(2,1,1)
]

El valor abierto se encuentra en el índice (0), por lo que:

[
R=ES=0
]

La relación resulta invertida respecto al cierre esperado:

[
E=1,\qquad O=1
]

---

# 9. Triangulación relacional

Una vez ordenadas, las tripletas pueden considerarse vectores relacionales:

* (FN) expresa la función o ángulo;
* (ES) expresa la orientación;
* (FO) expresa la forma o módulo.

Las formas se validan circularmente mediante tres TriGates ordinarios. Cada forma se reconstruye a partir de las otras dos y de la función asociada al vértice que se intenta cerrar:

[
T_1=(A=FO_1,;B=FO_2,;M=FN_3;;R=FO_3)
]

[
T_2=(A=FO_2,;B=FO_3,;M=FN_1;;R=FO_1)
]

[
T_3=(A=FO_3,;B=FO_1,;M=FN_2;;R=FO_2)
]

Los resultados reconstruidos recuperan el orden canónico de las formas:

[
(FO_1^*,FO_2^*,FO_3^*)=(R_{T_2},R_{T_3},R_{T_1})
]

La triangulación no introduce una función nueva. Consiste en tres TriGates ordinarios dispuestos circularmente para validar una estructura relacional.

---

# 10. Dimensiones superiores

El mismo procedimiento se aplica por separado a los valores que comparten un mismo rol:

* tres TriGates para (FN);
* tres TriGates para (FO);
* tres TriGates para (ES).

Los tres resultados (R) obtenidos forman una nueva tripleta en el nivel fractal superior.

Esta tripleta recibe el nombre de:

* dimensión superior;
* tripleta superior;
* vector superior;
* (DS).

La nueva tripleta debe ordenarse mediante la misma función y relacionarse recursivamente con otras tripletas del mismo nivel.

Los estados (E) producidos durante la operación forman:

[
DE=(E_1,E_2,E_3)
]

denominada **dimensión de coherencia**.

De igual modo, las orientaciones (O) forman:

[
DO=(O_1,O_2,O_3)
]

denominada **dimensión de ordenación**.

El conjunto:

[
(DS,DE,DO)
]

constituye el conocimiento necesario para extender o reconstruir una tripleta cuando solo se dispone de su dimensión superior.

---

# 11. Caras de operación

Cada mecanismo completo de operación se denomina **cara**.

Inicialmente existen tres caras fundamentales:

* (SO_{\text{entrada}}): contiene los datos recibidos.
* (SO_{\text{conocimiento}}): contiene el conocimiento recuperado del diccionario.
* (SO_{\text{salida}}): representa la estructura que el sistema intenta producir.

La cara de salida debe cumplir dos condiciones:

1. Ser coherente con las caras de entrada y conocimiento.
2. Mantener la misma dirección, sentido o fase relacional.

A partir de estas tres caras se construyen otras tres.

## 11.1. Cara de dirección

Se agrupan las dimensiones superiores:

[
DS_{\text{entrada}},\quad DS_{\text{conocimiento}},\quad DS_{\text{salida}}
]

Estas forman una nueva Semilla Operativa:

[
SO_D
]

que determina la dirección conjunta.

## 11.2. Cara de coherencia

Se agrupan las dimensiones de coherencia:

[
DE_{\text{entrada}},\quad DE_{\text{conocimiento}},\quad DE_{\text{salida}}
]

Estas forman:

[
SO_C
]

que evalúa la coherencia global.

## 11.3. Cara de ordenación

Se agrupan las dimensiones de ordenación:

[
DO_{\text{entrada}},\quad DO_{\text{conocimiento}},\quad DO_{\text{salida}}
]

Estas forman:

[
SO_O
]

que conserva la orientación y continuidad del proceso.

Finalmente, (SO_D), (SO_C) y (SO_O) comparten nuevamente sus dimensiones (DS), (DE) y (DO), generando una última Semilla Operativa de armonización:

[
SO_H
]

Esta semilla representa el cierre completo de la operación.

---

# 12. Relación con el diccionario

Todas las relaciones entre una Semilla Operativa y sus tripletas de conocimiento se calculan inicialmente en la cara de entrada.

Una vez calculadas, se almacenan en el diccionario. Las demás caras no pueden inventarlas de nuevo: únicamente pueden recuperar, reutilizar, contrastar o competir con relaciones previamente registradas.

El diccionario se indexa mediante:

[
DS,\quad DE,\quad DO
]

El índice utilizado depende de la orientación de la búsqueda.

Las entradas se ordenan según su último encuentro o utilización, de manera que el conocimiento más recientemente validado tenga prioridad sin eliminar necesariamente las alternativas anteriores.

Una misma estructura puede disponer de varias representaciones. Estas representaciones compiten durante la resolución y una contradicción puede hacer que el sistema pruebe una alternativa diferente.

---

# 13. Cierre de la ventana

El procedimiento evalúa todas las tripletas presentes en las Semillas Operativas de la ventana.

El encadenamiento produce una última semilla:

[
SO_{WS}
]

Esta semilla representa el resultado completo del cálculo de la ventana.

Su dimensión (DE) determina el estado global:

[
DE_{WS}=
\begin{cases}
0 & \text{ventana coherente}\
1 & \text{ventana incoherente}\
2 & \text{ventana ambigua}
\end{cases}
]

Si la ventana es coherente, el tensor emergente sintetiza el conjunto de dimensiones superiores:

[
T_E\leftarrow{DS}
]

Si permanece abierta, el tensor emergente conserva la información de coherencia necesaria para continuar:

[
T_E\leftarrow{DE}
]

No obstante, el tensor que asciende debe mantener también sus dimensiones auxiliares y su procedencia:

[
T_E=(DS_E,DE_E,DO_E,\Pi_E)
]

Así, la síntesis no pierde la información necesaria para reconstruir, validar o revisar el proceso que la produjo.

---

# 14. Evolución del tensor desconocido

El tensor (U) aparece en las Semillas Operativas de salida de la ventana.

Su contenido se resuelve progresivamente mediante búsquedas en el diccionario, comenzando por los niveles más bajos:

[
\text{TriGate}
\rightarrow
\text{tripleta}
\rightarrow
SO
\rightarrow
\text{tensor}
]

La expansión de cada valor abierto sigue la regla:

[
0\longrightarrow0
]

[
1\longrightarrow1
]

[
2\longrightarrow{0,1,2}
]

Los valores determinados permanecen estables. Solo el valor (2) abre un espacio de búsqueda.

El sistema intenta cerrar primero las relaciones elementales. Los cierres obtenidos forman tripletas; las tripletas forman Semillas Operativas; las Semillas Operativas forman tensores. De esta manera, el conocimiento emerge gradualmente desde los niveles inferiores.

El tensor (U) no es un tercer dato observado. Es el espacio abierto de conocimiento que la ventana intenta recuperar, reconstruir o mantener como carry.

---

# 15. Arquitectura completa

La arquitectura operativa de Aurora puede resumirse mediante la cadena:

[
\boxed{
\text{TriGate}
\rightarrow
\text{tripleta ordenada}
\rightarrow
SO
\rightarrow
\text{caras}
\rightarrow
\text{tensor}
\rightarrow
\text{ventana}
\rightarrow
T_E
\rightarrow
\text{nivel superior}
}
]

La misma lógica se reproduce en todas las escalas.

Cada TriGate intenta cerrar su pequeño espacio relacional. Los valores compartidos propagan los cambios hacia los TriGates conectados. Las tripletas sintetizan esos cierres. Las Semillas Operativas los organizan fractalmente. Los tensores conservan la síntesis y su procedencia. Finalmente, las ventanas determinan qué estructuras emergen, cuáles continúan abiertas y cuáles deben separarse.

No existe necesariamente un controlador central que resuelva todo el problema. La solución global emerge de:

* la resolución local;
* la propagación de eventos;
* la redundancia de relaciones;
* la búsqueda en el diccionario;
* la competencia entre alternativas;
* el cierre progresivo de los valores (2).

En Aurora, el valor (2) no representa únicamente desconocimiento. Representa el espacio todavía abierto en el que el sistema puede aprender, deducir, reorganizar su conocimiento y producir una nueva estructura coherente.
