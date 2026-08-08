# Resultados de Aurora compacto 0.18.0-rc2

Auditoría ejecutada el 6 de agosto de 2026.

## Validación

- 150/150 pruebas unitarias, fractales, secuenciales, deductivas, de red y de
  entrenamiento.
- 243 configuraciones dirigidas del TriGate.
- 46.875 caras, 46.875 ventanas y 46.875 controles en total: 15.625 por
  dirección.
- Diccionario y red consultados mediante el mismo dominio deductivo de `B`.
- Control superior comprobado para sus nueve significados
  `HDS/HDE/HDO`.
- Tokens simples comprobados con `DO=DE=222` y `DS` explícito.
- Inventario inicial de caracteres comprobado como tensores reejecutables de
  13 tripletas y 39 trits.
- Crecimiento de secuencias comprobado para cierre, `carry`, contradicción,
  recurrencia y ascenso a más de un nivel.
- Competencia exhaustiva comprobada para cierres solapados, empate contextual,
  selección por recurrencia y repetición en el nivel fractal superior.
- Entrenamiento incremental comprobado para observación, evaluación sin
  mutación, evidencia textual no operativa y reanudación exacta desde JSON.
- Competencia de lecturas comprobada para `c`, `g` e `y`, con conservación de
  empates, transferencia contextual y persistencia exacta.
- Selección descendente comprobada frente al recorrido exhaustivo, con
  conservación de empates y métricas explícitas de activación y poda.
- Ejecutor relacional universal comprobado con semillas tensoriales,
  propagación por eventos, alternativas exactas y reejecución completa.
- Diccionario tensorial comprobado en niveles `9→3→1`, con rutas distintas para
  aprendizaje e inferencia, deducción orientada por `O` y conservación de las
  nueve alternativas cuando el orden permanece abierto.
- Cara de salida comprobada con búsquedas `111`, `110`, `101`, `011`, `100`,
  `000` y `112`, escritura de una sola ausencia y relectura inmediata.
- Orientación comprobada desde tripleta, SO y tensor hasta ventana y control,
  con carry completo y enlace directo `O→C`.
- Una única `Unit(K)` recuperada por identidad desde sus tres índices `DO`,
  `DE` y `DS`.
- Paso de ventana comprobado sin clasificador de movimiento: `O=DO[C]`
  selecciona la conexión y se convierte directamente en el siguiente `C`.
- Apertura comprobada conservando simultáneamente la conexión del nivel actual
  y la del nivel superior.
- Raíz `9→3→1` consultada desde sus tres canales y reejecutada con toda su
  procedencia.
- Ventana canónica comprobada como `(A,B,2)` en cierre, apertura e
  incoherencia, con un único tensor nuevo consumido por continuación.
- Prioridad `R=2 → apertura` comprobada incluso cuando `E` conserva el residual
  `000`, sin producir una contradicción falsa.

## Resultado de la ventana corregida 0.18.0-rc2

Los tres casos canónicos se reprodujeron sobre unidades causales:

```text
(A,B,2₀) -> 2ₑ coherente   -> superior U(A,B,2ₑ)
(A,B,2₀) -> 2ₑ ambiguo     -> (2ₑ,siguiente,2₀)
(A,B,2₀) -> incoherencia   -> superior A + (B,siguiente,2₀)
```

El tensor `2₀` es una unidad completa `K=(222,222,222)`, no un valor nulo del
lenguaje anfitrión. Cada nuevo intento crea otra unidad abierta. Su estado
evolucionado `2ₑ` conserva como descendientes `A`, `B` y `2₀`. Cuando la
relación cierra, la unidad superior es otra identidad causal: conserva
`(A,B,2ₑ)` y vuelve a ejecutarse mediante la misma cara.

La continuación abierta y la contradictoria consumen exactamente un tensor
nuevo. Esto sustituye el prototipo histórico `(carry,siguiente,siguiente)` y
evita llenar con una entrada determinada el lugar destinado al resultado.
En ambos casos el `DO` de la unidad retenida se hereda como fase de la ventana
siguiente, verificando `O[t]→C[t+1]` también durante el desplazamiento.

La auditoría enumera las 625 parejas posibles de las 25 tripletas procesables:
137 cierran, 464 permanecen abiertas y 24 son incoherentes. Dos de las 24 son
resultados no ordenables (`012` y `102`) que un voto aislado de `DE` habría
cerrado incorrectamente.
Todos los tensores evolucionados reejecutan; las 137 emergencias coherentes también reejecutan; y
todas las transiciones conservan por identidad la unidad que asciende o
continúa.

## Resultado histórico release candidate 0.18.0-rc1

Una unidad emergente causal produjo:

```text
DO = 210
DE = 220
DS = 202
```

El diccionario la almacenó una sola vez. Tres consultas independientes —una
por `DO`, otra por `DE` y otra por `DS`— devolvieron estado `111`, el mismo
objeto y el mismo `K` completo. Las orientaciones emitidas fueron `210`,
exactamente los tres trits de `DO` leídos desde sus respectivos índices.

La topología de prueba contenía una conexión al nivel actual, otra al nivel
superior y un puerto abierto que conservaba ambas. Presentar la misma unidad
desde `C=0,1,2` produjo:

```text
C recibido = 012
O emitido  = 210
C siguiente= 210
```

`O=0` presentó la unidad en el nivel actual; `O=1`, en el nivel superior; y
`O=2` conservó ambos destinos. Las tres presentaciones mantuvieron la identidad
del objeto y su procedencia. Cambiar únicamente `DE` no alteró ninguna ruta.

Nueve copias causales de la unidad se promovieron como `9→3→1`. La raíz de
nivel 2 conservó nueve hojas, reejecutó todas sus caras y volvió a recuperarse
como la misma identidad desde sus tres índices.

El nuevo núcleo no importa ni consulta `growth.py` u `output_face.py`, no
ejecuta `classify_de()` y no contiene `GrowthAction`, `OutputAction`,
`ASCEND`, `CARRY`, `SHIFT` o `CRYSTALLIZE`. La interpretación carry/emergencia
procede exclusivamente de la conexión tensorial seleccionada.

## Orientación fractal completa 0.17

La enumeración de todas las tripletas y sus tres fases confirmó que, siempre
que la ordenación es resoluble, `O` selecciona exactamente la posición de
`ES`. La selección vertical conserva la misma invariante en la relación
inferior indicada por `O↑`.

Una SO compilada desde un tensor-programa recuperó exactamente la misma
instrucción `K=(DO,DE,DS)`. Una única `Unit` con `DO=012` fue presentada desde
los índices `0`, `1` y `2`; produjo las tres orientaciones correspondientes sin
ser reconstruida ni cambiar de identidad.

La ventana abierta conserva ahora `DO`, `DE`, `DS`, dirección, fotografía y
los tres progenitores en un carry reejecutable. El control superior proyecta
los paquetes finales de `HDS/HDE/HDO` como otro `K`; sus trits `DS` son las
lecturas de operación, coherencia y alcance, y las dos etapas del control
vuelven a reejecutarse desde sus caras preservadas.

La prueba no impone una tabla `orientación→movimiento`. Ascender, extender o
desplazar deberá resultar de dónde se vuelvan a presentar las salidas, no de
una etiqueta añadida al tensor.

## Cara de salida lectora-escritora 0.16

Tres requisitos consultaron un único bosque desde sus respectivos índices
`C=0`, `C=1` y `C=2`. Cuando los tres estaban presentes, la tripleta `111`
continuó sin modificar la memoria. Los tres casos con una única ausencia
(`011`, `101`, `110`) incorporaron exclusivamente esa salida y la relectura
produjo `111`.

El tensor nuevo del experimento no se redactó durante la resolución: se
recuperó de un disparo causal y conservó sus nueve unidades reejecutables. Tras
añadirlo a la raíz existente, la frontera pasó de `[0,0,1]` a `[1,0,1]`; tanto
la raíz anterior como la unidad nueva continuaron disponibles.

Con dos ausencias (`100`) o tres (`000`), el diccionario permaneció idéntico y
se devolvieron los tres tensores. El caso `112` conservó nueve alternativas y
no escribió: apertura y ausencia siguieron siendo estados diferentes.

## Diccionario fractal orientado por C-O 0.15

Nueve programas con el mismo ejecutor formaron tres nodos y una raíz. El modo
operativo determinó la ruta en las dos escalas:

```text
C=0                  → 0→0
C=1                  → 1→1
C=2 con fase O=0     → 0→2
C=2 con fase O=2     → 2→2
```

La deducción no interpreta `2` como una tercera rama determinada. Consulta la
ordenación del átomo `DO` del nodo. Cuando los nueve programas usaron `DO=222`,
esa ordenación permaneció abierta y la consulta conservó las nueve alternativas
sin elegir una.

Otra prueba partió de nueve disparos reales con programas
`A,A,B | A,B,A | B,A,A`. Cada disparo reflejó su código; las ternas formaron
tres programas `A`; estos formaron una raíz `A`, y la raíz se ejecutó
directamente. El diccionario no recibió candidatos redactados manualmente ni
usó `sort`, máximos, soporte, recencia, pesos o umbrales.

## Nuevo resultado: educación en lugar de acciones ad hoc

La versión 0.12 introduce un segundo camino de ejecución que no importa ni usa
`GrowthAction`. Su bucle no contiene decisiones para ascender, transportar,
desplazar, segmentar o podar. Una semilla tensorial declara tres entradas, tres
salidas y una instrucción Aurora: la mayoría de `DS` determina `C` y `DO`
determina la fase.

El mismo ejecutor reproduce dos conductas del banco de pruebas:

```text
educación vertical:      9 señales → 3 caras → 1 cara
educación de apertura:   DE=222 → nueva presentación → DE=111
```

En el primer caso se producen cuatro disparos, una raíz `DS=000` de profundidad
dos y un punto fijo. En el segundo se producen dos disparos: la primera cara
queda abierta y su `DS` se combina con los dos elementos siguientes hasta
cerrar. Todas las señales emitidas vuelven a calcular exactamente su valor a
partir de la semilla y de sus tres progenitoras.

Cambiar únicamente el tensor de instrucción sobre tres entradas `000` también
produce un efecto observable: `C=0` conserva `DE=222`, mientras `C=1` produce
`DE=111`. El código del ejecutor es idéntico en ambos casos.

Este resultado demuestra que la presentación tensorial puede gobernar la
operación. Todavía no demuestra que Aurora aprenda autónomamente la topología:
las conexiones de estas dos educaciones se proporcionan manualmente.

## Primer vocabulario fractal de caracteres

El perfil 0.6 añade una raíz con tres ramas de rol y tres propiedades por rama.
Las propiedades inferiores cambian con la familia de la raíz, de modo que la
herencia no es una tabla plana:

- vocal → altura, posición, redondeamiento, silabicidad y acento;
- consonante → lugar, modo, fonación, estabilidad y realización;
- símbolo → frontera, pausa, contorno y fuerza prosódica.

El inventario español conserva alternativas para grafemas contextuales y
permite que dos caracteres compartan un patrón completo. `b` y `v`, por
ejemplo, pueden comenzar con el mismo tensor fonético sin convertirse en el
mismo token. La búsqueda por propiedades vuelve a ejecutar la deducción de
`B`; no añade distancia ni similitud.

## Experimento secuencial heredado

El ensayo determinista de 600 secuencias continúa reproduciendo el resultado de
0.4: 576 secuencias reconocidas como tensores completos, 48 relaciones nuevas
y coste lógico de 1 después de estabilizar cada distribución. El cambio en la
secuencia 300 vuelve a concentrar temporalmente el gasto en la novedad.

Este ensayo valida memoria estructural, competencia y lexicalización. No debe
confundirse con la realimentación completa del nuevo control emergente: el ciclo
secuencial todavía usa `transcend()` como perfil léxico compatible.

## Nuevo resultado estructural

La misma ecuación se ejecuta ya en dos escalas:

```text
D(A,M,R) = {B | Majority3(A,B,M)=R}
```

- En el diccionario local, `B` identifica una relación candidata.
- En la red, `B` identifica el tensor-ruta de un nodo candidato.

Una resolución remota correcta añade la ruta al directorio y la siguiente
consulta la reutiliza antes de recorrer los demás nodos. Esto implementa la
especialización por experiencia sin añadir similitud geométrica.

## Ventana de crecimiento

La versión 0.7 ejecuta los dos movimientos fractales de una secuencia:

```text
DE=1 -> cierre  -> ascenso vertical
DE=2 -> carry   -> extensión horizontal con dos unidades nuevas
DE=0 -> rechazo -> desplazamiento horizontal de la ventana
```

La prueba mínima abierta usa cinco unidades. Las tres primeras producen
`carry`; el segundo intento recibe ese `carry` y las dos unidades siguientes,
cierra y devuelve una unidad con la procedencia completa de las cinco. Otra
prueba hace ascender nueve unidades como `9 -> 3 -> 1` mediante la misma cara.

Cada cierre nuevo se guarda como una relación completa y reejecutable. En la
segunda observación, la relación no se duplica: aumenta su contador de usos y
su prioridad temporal. Las aperturas y contradicciones no se lexicalizan. En
el perfil 0.7, los grafemas contextuales todavía requerían una lectura
explícita; 0.10 sustituye esa frontera por competencia entre lecturas.

## Competencia solapada

La versión 0.8 ejecuta la ventana desde todos los inicios posibles y conserva
cada cierre exacto en el diccionario. Las combinaciones no solapadas forman un
grafo de segmentaciones; el runtime compara todas las rutas compatibles sin
materializar una lista exponencial de rutas dominadas.

En la prueba abstracta `AAB·AAB·AAB` se observan siete cierres solapados, tres
relaciones distintas y diecinueve segmentaciones compatibles. Sus soportes
finales son:

```text
AAB = 3
ABA = 2
BAA = 2
```

La única rama superior es `AAB | AAB | AAB`; después, sus tres unidades
repiten la competencia y forman una raíz reejecutable. En `AABB` sin memoria,
en cambio, `AAB | B` y `A | ABB` quedan empatadas. Entrenar previamente una de
las relaciones selecciona únicamente su rama, pero la alternativa infrecuente
continúa almacenada.

La selección no usa suma ponderada, distancia ni frecuencia mínima. Compara,
en orden, la recurrencia exacta, la anchura comprimida y la procedencia cerrada.
La recencia no rompe empates semánticos, evitando que el orden accidental de
ejecución imponga una segmentación.

## Primer entrenamiento con secuencias reales

La versión 0.9 observa 12 secuencias españolas durante tres épocas. El corpus
no contiene fronteras silábicas o léxicas esperadas: solo caracteres, espacios
y signos con sus tensores iniciales. El resultado reproducible es:

```text
observaciones = 36
relaciones exactas = 59
consulta "luna": ganadores antes = 2
consulta "luna": ganadores después = 1
rama activa después = "una"
```

Los cierres con mayor recurrencia fueron:

| Forma observada | Soporte | Observaciones |
|---|---:|---:|
| `una` | 24 | 21 |
| ` lu` | 21 | 21 |
| `lun` | 21 | 21 |
| `na ` | 21 | 18 |
| `a l` | 18 | 18 |
| `ale` | 18 | 18 |
| `la ` | 18 | 18 |
| `sal` | 18 | 18 |

Antes de entrenar, `luna` mantiene empatadas las ramas `lun|a` y `l|una`.
La presencia adicional de `una` en contextos diferentes eleva el soporte de
su tensor exacto y rompe el empate. `lun` no se borra ni se degrada; continúa
en el diccionario como candidata válida para otro contexto.

Este resultado demuestra aprendizaje de prioridad estructural, no
silabificación. Las formas de la tabla son evidencia para el auditor y nunca
entran en el cálculo de cierre.

## Lecturas contextuales aprendidas

La versión 0.10 materializa todas las lecturas disponibles de un carácter y
ejecuta la competencia fractal ordinaria en cada rama desde la misma memoria
inmutable. Antes de recibir experiencia diferenciadora, las dos ramas de cada
consulta permanecen empatadas. Repetirlas sin información nueva no fabrica una
preferencia.

El experimento controlado aporta seis cierres fonéticos validados durante
cuatro épocas y evalúa otras secuencias sin declarar sentidos:

```text
observaciones = 24
relaciones exactas = 18
ganadores por consulta antes = 2
ganadores por consulta después = 1
```

| Consulta | Lectura emergente | Evidencia contextual reutilizada |
|---|---|---|
| ` cama` | `c=velar` | ` ca` aprendido en ` casa` |
| ` cero` | `c=coronal` | ` ce` aprendido en ` cena` |
| ` gana` | `g=voiced` | ` ga` aprendido en ` gato` |
| ` gesto` | `g=fricative` | ` ge` aprendido en ` gente` |
| ` soy ` | `y=vowel` | `oy ` aprendido en ` hoy ` |
| ` ya ` | `y=consonant` | cierre validado completo |

La comparación comienza por cierres activos que contienen la posición
ambigua, de modo que una relación recurrente situada en otra parte de la frase
no puede ocultar la diferencia entre las lecturas. Las ramas perdedoras se
conservan con soporte de génesis, pero no reciben reutilizaciones exitosas.
Los cierres idénticos presentes en varias ramas mutuamente excluyentes cuentan
una sola vez por observación.

Esto prueba selección y transferencia contextual después de experiencia
validada. No prueba inducción fonética desde ortografía aislada: cuando el
flujo no contiene señal diferenciadora, Aurora conserva correctamente la
apertura.

## Poda fractal descendente

La versión 0.11 recorre la procedencia de los cierres almacenados y recupera
los tensores inferiores que los formaron. Una coincidencia contextual actúa
como ruta superior y restringe los sentidos compatibles antes de ejecutar el
crecimiento. El texto visible y la evidencia de auditoría no participan en
esta selección.

Las seis consultas del ensayo 0.10 pasan de dos lecturas posibles a una
ejecución y conservan el mismo ganador que el recorrido exhaustivo. El caso
combinado mide la reducción multiplicativa:

```text
flujo = " cama gesto soy "
lecturas posibles = 8
lecturas ejecutadas = 1
lecturas podadas = 7
tasa de activación = 1/8
ganador descendente = ganador exhaustivo
```

Sin memoria diferenciadora, ` casa` sigue ejecutando sus dos lecturas. Si se
entrenan con la misma prioridad los cierres velar y coronal del mismo contexto,
ambos permanecen activos. La poda solo ocurre cuando una relación superior
cerrada rompe realmente la equivalencia.

## Persistencia

El estado completo —diccionario, lexicón, soporte, reloj y evidencia— se guarda
en un checkpoint JSON versionado. Una restauración produce un estado idéntico
y todas sus relaciones vuelven a superar la reejecución. Esto permite continuar
un entrenamiento sin reiniciar la memoria ni introducir un formato binario
opaco.

## Límite medido

En las unidades simples, `DE` y `DO` comienzan abiertos. Por ello, una sola
proyección estática de C4–C6 tiende a conservar apertura en `HDO`; el cambio
local → red → parada debe surgir de la realimentación entre intentos, no de una
lectura aislada del estado inicial. Conectar ese bucle al runtime es el próximo
hito de ingeniería.

El motor ya hace crecer secuencias, acumula recurrencia, compite entre cierres
solapados, conserva entrenamiento y usa cierres superiores para evitar ramas
inferiores incompatibles. El siguiente límite es medir estabilidad y
retrocesos en un corpus amplio, incorporar una fuente real de experiencia
fonética y conectar la realimentación completa de `HDS/HDO`. Todavía no hay
evidencia suficiente para afirmar que cada cierre corresponde a una sílaba
humana.

## Tensor-programa 0.13

El perfil 0.13 codifica la presentación completa en nueve tripletas y corrige
la tercera dirección operativa: `DE=111,DS=222` es una instrucción cerrada de
deducción, mientras `DE=222,DS=222` permanece indeterminada.

Dos copias de un programa `A` y una alternativa `B` se presentaron posición por
posición a nueve caras. La síntesis reconstruyó exactamente `A`, conservó la
procedencia de las tres candidatas y el programa emergente volvió a ejecutarse
correctamente. No intervino ningún contador de recurrencia ni selección por
máximo.

En la prueba negativa, tres programas válidos produjeron una dirección de
salida `102`, imposible como dirección literal ordenada. La síntesis y sus tres
antecedentes se conservaron, pero no se permitieron como programa ejecutable.
El cierre determina si el código puede operar; el anfitrión no fuerza una
elección.

## Código propuesto por procedencia 0.14

Cada semilla tensorial conserva ahora las nueve unidades educativas que la
originaron. Tras ejecutarse, un disparo refleja esas unidades como programa y
verifica que sus entradas, salidas e instrucción coinciden con la ruta causal
real. La serialización JSON conserva también la procedencia interna.

Tres ejecuciones `A,A,B` sobre la misma ventana causal produjeron tres
programas reflejados y las mismas nueve caras sintetizaron nuevamente `A`. El
programa emergente se ejecutó y publicó `DS=000` en la dirección aprendida. No
se llamó a `ProgramTensor.author()` para formar los candidatos ni se usaron
contadores, soporte, pesos, umbrales o máximos.

Dos ejecuciones de una ventana y una tercera de otra no produjeron ninguna
inducción. En la prueba incompatible, tres rutas válidas generaron la dirección
imposible `102`: las tres hipótesis permanecieron en la procedencia y el código
emergente no se activó.

La regresión 0.14 alcanzó 108 pruebas, 0.15 alcanzó 116, 0.16 alcanzó 125 y
0.17 alcanzó 133 y 0.18.0-rc1 alcanzó 143. El candidato 0.18.0-rc2 alcanza 151,
conserva `K` completo, lo consulta desde sus tres canales y hace que la ventana
repita la relación `(A,B,2)` sin una política de segmentación independiente. La
frontera siguiente es encadenar esta transición en todos los niveles con
topologías aprendidas por el propio sistema.
