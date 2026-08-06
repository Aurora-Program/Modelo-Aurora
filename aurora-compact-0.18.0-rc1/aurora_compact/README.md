# Aurora compacto 0.18.0-rc1

Release candidate de la arquitectura Aurora cerrada el 6 de agosto de 2026.
El paquete convierte las reglas ternarias en objetos auditables, conserva la
procedencia fractal y prueba que diccionario y red pueden usar la misma
deducción sin embeddings, distancias ni umbrales de similitud.

El contrato candidato reduce todas las escalas a una única transición:

```text
C → leer K[C] → O=DO[C] → conexión[O] → C siguiente
```

El diccionario guarda un único `K=(DO,DE,DS)` y permite recuperarlo desde sus
tres canales. La ventana entrega esa misma unidad a la conexión seleccionada
por `O`: si la conexión pertenece al nivel actual observamos carry; si
pertenece al nivel superior observamos emergencia; si la orientación permanece
abierta se conservan ambos destinos. El núcleo RC no decide el movimiento a
partir de `DE` ni usa clases de acción semántica. Véase
`RELEASE_CANDIDATE.md`.

El candidato continúa la rama del ejecutor relacional que no conoce
segmentación, `carry`, ascenso ni poda. Las semillas operativas son tensores y
la educación decide únicamente qué tres señales se presentan juntas y dónde
se vuelven a presentar `DO`, `DE` y `DS`. Las capas 0.7–0.11 se conservan como
banco de pruebas, pero ya no se confunden con el runtime definitivo.

No es todavía un modelo lingüístico completo ni un transporte P2P de
producción. Los programas candidatos nacen de disparos con procedencia causal
y se realimentan en un diccionario ternario. La cara de salida experimental
consulta tres rutas en paralelo, cristaliza una única ausencia determinada y
devuelve las salidas cuando dos rutas no encuentran conocimiento.

0.17 hizo explícita la orientación fractal completa. En una tripleta, `O`
determina `ES`; entre niveles, la orientación emitida puede entrar sin
traducción como `C`; una ventana abierta conserva el `K` completo y el control
vuelve a proyectarse como una unidad ordinaria `(DO,DE,DS)`. Véase
`ORIENTATION.md`. 0.18.0-rc1 completa ese paso: `C` selecciona uno de los tres
canales del mismo `K`, `O=DO[C]` selecciona una conexión y la ventana actúa
únicamente como frontera entre escalas.

## Núcleo release candidate

`fractal_kernel.py` contiene la frontera canónica del RC:

- `FractalTensorDictionary` promueve unidades `1–3–9` y recupera la misma
  identidad desde `DO`, `DE` o `DS`;
- `FractalTopology` conserva tres puertos tensoriales sin interpretar su
  significado;
- `FractalWindow` sintetiza una unidad y la presenta intacta al puerto elegido
  por `O`;
- `UnitPassage.next_c` es literalmente la orientación saliente;
- `pass_triplet()` usa el mismo `O` que determina `ES` y conserva todas las
  orientaciones de una tripleta todavía abierta.

Los prototipos anteriores siguen incluidos para reproducibilidad, pero sus
acciones Python no forman parte del contrato candidato.

## Diccionario fractal C-O

El perfil 0.15 convierte el modo operativo en acceso estructural al
diccionario. La misma regla se repite en cada nivel:

| `C` | Acceso |
|---:|---|
| `0` | rama de aprendizaje `0` |
| `1` | rama de inferencia `1` |
| `2` | decisión abierta; el átomo `DO` determina `O` |

Cada tres programas forman un nodo y cada tres nodos forman una raíz. El cierre
emergente se incorpora automáticamente al nivel siguiente. Si `C=2` y `DO`
permanece abierto, el diccionario conserva todas las alternativas; no escoge
por posición accidental, contador o máximo. Véase `FRACTAL_DICTIONARY.md`.

## La salida consulta y escribe

Cada tensor de salida busca desde su propio índice `C`. Las tres búsquedas
producen una tripleta de estados `H`, donde `0` es ausencia, `1` cierre y `2`
apertura. La regla demostrada es:

```text
111 → continuar
110 / 101 / 011 → cristalizar solo el ausente y continuar
000 / 100 / 010 / 001 → devolver los tres tensores
cualquier H con 2 → conservar apertura y alternativas
```

La cristalización reutiliza el tensor causal ya producido; no llama a
`ProgramTensor.author()` ni construye una hipótesis sustitutiva. Véase
`OUTPUT_FACE.md`.

## Contrato operativo congelado

El TriGate conserva `A` como ancla y transforma una de tres celdas:

| `C` | Celda | Operación |
|---:|---|---|
| `0` | `M` | Aprender |
| `1` | `R` | Inferir |
| `2` | `B` | Deducir o buscar |

C4, C5 y C6 son caras ordinarias. Sus canales vuelven a proyectarse como
`HDS`, `HDE` y `HDO`; no existe un armonizador externo ni se compara contra
`012`, `111` o `000` como objetivos impuestos.

| Resultado superior | `0` | `1` | `2` |
|---|---|---|---|
| `R(HDS)` | Aprender | Inferir | Deducir/buscar |
| `R(HDE)` | Incoherente | Coherente | Ambiguo |
| `R(HDO)` | Diccionario local | Red Aurora | Detener |

## Buscar es deducir

Una consulta conoce `A`, `M` y `R` y recupera todos los tensores `B` que
satisfacen:

```text
Majority3(A, B, M) = R
```

La consulta canónica `A=R=tensor`, `M=222` exige coincidencia en las
coordenadas determinadas y mantiene abiertas las coordenadas `2`. Si se desea
buscar el valor literal `2`, una relación complementaria lo deduce de manera
única. Aurora conserva así la diferencia entre el trit `2` y un dominio con
varias candidatas.

La red de `routing.py` repite exactamente esa búsqueda. En alcance local el
payload es una relación `(I,K,S,C)`; en alcance de red es un nodo. Cuando un
nodo remoto cierra la consulta, su tensor-ruta se aprende y se reutiliza en la
siguiente búsqueda.

## Tensores de tokens simples

Un token simple nace como:

```text
T_token = (DO=222, DE=222, DS=DS_token)
```

`tokens.py` permite asignar tensores explícitos, reservarlos en orden ternario
y asociar más de un tensor al mismo texto mediante sentidos diferentes. La
función `numeric_lexicon()` hace coincidir una lista ordenada de nombres
numéricos con `000, 001, 002, 010...`.

## Caracteres como tensores fractales

`characters.py` convierte cada carácter conocido en un tensor operativo
`1–3–9`:

```text
raíz del carácter                         1 tripleta
├── estructura                            3 propiedades inferiores
├── función                               3 propiedades inferiores
└── forma                                 3 propiedades inferiores
                                          ─────────────────────────
total: raíz + 3 ramas + 9 propiedades     13 tripletas = 39 trits
```

Las posiciones físicas no fijan para siempre `ES/FN/FO`: cada rama lleva su
enlace semántico y puede reordenarse sin perder sus propiedades. La familia de
la raíz determina el espacio inferior:

| Familia | Estructura inferior | Función inferior | Forma inferior |
|---|---|---|---|
| Vocal | familia, altura, posición | redondeamiento, silabicidad, acento | caja, marca, composición |
| Consonante | familia, lugar, modo | fonación, estabilidad, realización | caja, marca, composición |
| Símbolo | familia, frontera, pareja | pausa, contorno, fuerza | espaciado, repetición, visibilidad |

Cada propiedad inferior vuelve a ser una tripleta de predicados. Sus valores
mantienen la semántica global `0=no`, `1=sí`, `2=abierto`; `2` no se reutiliza
como una etiqueta arbitraria para «símbolo». Las ramas y la raíz se sintetizan
con `synthesize()` y toda la procedencia puede reejecutarse.

`DS` de la raíz es una síntesis, no un identificador exclusivo. Dos caracteres
pueden producir el mismo resumen superior y conservar árboles inferiores
distintos; por eso búsqueda y reejecución usan el tensor completo de trece
tripletas. Esto aplica al carácter la regla general de Aurora: `DS` localiza un
espacio de candidatas y la procedencia fractal determina cuál cierra.

El vocabulario inicial incluye vocales españolas, consonantes y signos de
puntuación. Grafemas contextuales como `c`, `g` e `y` conservan tensores
competidores. Por ejemplo, `y` puede tener un tensor consonántico y otro
vocálico. `CharacterQuery` busca propiedades mediante la misma deducción del
TriGate empleada por el diccionario.

## Crecimiento horizontal y vertical (prototipo histórico 0.7–0.11)

`growth.py` conecta los tensores de caracteres con la ventana deslizante. No
contiene un silabificador ni una tabla de combinaciones permitidas. Cada
intento vuelve a ejecutar `synthesize()` sobre tres unidades del mismo nivel y
deja que `DE` determine el movimiento. Esta fue la hipótesis experimental de
0.7 y no forma parte del contrato 0.18.0-rc1:

| Estado de `DE` | Movimiento | Consecuencia |
|---|---|---|
| `111` | Vertical | La relación cierra, se aprende y asciende como una unidad |
| `000` | Horizontal | La agrupación se rechaza y la ventana se desplaza |
| `222` o mixto | Horizontal | La relación se conserva como `carry` y recibe dos unidades más |

Una secuencia abierta continúa exactamente así:

```text
(x1, x2, x3) -> carry
(carry, x4, x5) -> nuevo intento
```

Tres cierres vuelven a ocupar las posiciones de una ventana superior. El
runtime repite la misma operación hasta obtener una raíz o llegar a una
frontera que necesita más contexto.

Al principio pueden cerrar muchas agrupaciones. Cada cierre nuevo se conserva
como una relación reejecutable `(I,K,S,C)`; cada repetición promociona esa
misma relación. La recurrencia no borra alternativas raras: les hace perder
prioridad frente a los cierres que vuelven a funcionar.

La versión 0.8 ejecuta la competencia solapada completa. `compete_level()`
inicia la misma ventana en todas las posiciones del flujo. Una rama abierta se
extiende por `carry`; una rama contradictoria se detiene en ese inicio; una
rama cerrada entra en el diccionario. Después, un grafo acíclico conserva todas
las candidatas y compara exhaustivamente las segmentaciones no solapadas.

No se calcula una puntuación ponderada ni se aplica un umbral. La prioridad es
lexicográfica y estructural:

1. soporte de recurrencia de la relación exacta;
2. anchura que esa relación comprime;
3. cantidad de procedencia cerrada por la segmentación completa.

La recencia se conserva como dato del diccionario, pero no rompe un empate
semántico entre segmentaciones diferentes. Si dos hipótesis tienen la misma
prioridad, ambas permanecen como frentes activos hasta que otro contexto
reutilice una de ellas. Solo una segmentación ganadora, completa y única puede
ascender al nivel siguiente.

Por ejemplo, la secuencia abstracta `AAB·AAB·AAB` produce siete cierres
solapados y diecinueve segmentaciones compatibles. Las relaciones `AAB`, `ABA`
y `BAA` alcanzan soporte `3`, `2` y `2`; por ello asciende de forma única
`AAB | AAB | AAB`. En cambio, `AABB` sin historia previa conserva empatadas
`AAB | B` y `A | ABB`.

La entrada estricta `compete_text()` sigue permitiendo fijar una lectura para
experimentos controlados. La entrada operativa `compete_contextual_text()`
desciende primero por los cierres aprendidos, materializa solo las lecturas que
siguen siendo compatibles y ejecuta en ellas la misma competencia fractal.
Sin una relación diferenciadora conserva todo el espacio abierto.

```python
from aurora_compact import growth

result = growth.grow_text("aaaaaaaaa")
assert [len(level.emerged) for level in result.growth.levels] == [3, 1]
assert result.growth.complete

open_result = growth.grow_text("hhh")
assert open_result.growth.levels[0].attempts[0].action.value == "carry"
```

Esta versión prueba el mecanismo de crecimiento, la memoria de recurrencia y
la competencia entre segmentaciones. No afirma que los cierres del inventario
fonético inicial reproduzcan ya la silabificación humana.

## Entrenamiento incremental

`training.py` convierte la competencia 0.8 en un ciclo operativo de corpus sin
añadir otra regla al modelo:

```text
texto -> competencia ordinaria -> diccionario inmutable -> siguiente texto
```

Cada observación:

1. materializa sus caracteres como tensores `1–3–9`;
2. conserva todos los cierres solapados, no solo el ganador;
3. promociona las relaciones exactas que vuelven a cerrar;
4. avanza un reloj lógico reproducible;
5. registra las formas visibles como evidencia de auditoría;
6. devuelve un nuevo `TrainingState` sin modificar el anterior.

Las formas textuales no participan en la búsqueda ni en la competencia. Solo
permiten inspeccionar qué secuencias originaron cada tensor. El aprendizaje
sigue dependiendo de la unidad fractal completa y de su soporte en el
diccionario.

```python
from aurora_compact import training

state = training.TrainingState()
step = training.observe_text(state, "una luna.")

# El estado anterior sigue vacío; el nuevo conserva el aprendizaje.
assert len(state.dictionary.entries) == 0
assert len(step.state.dictionary.entries) > 0

# Evaluar no confirma los nuevos usos en memoria.
probe = training.evaluate_text(step.state, "luna")
assert len(probe.growth.levels[0].winners) == 1

training.save_state(step.state, "aurora-state.json")
restored = training.load_state("aurora-state.json")
assert restored == step.state
```

Un `TrainingSample` puede aportar un sentido validado como experiencia de
arranque. No crea una regla permanente: solo permite que el cierre resultante
entre en el diccionario. Las muestras posteriores pueden omitir el sentido y
reutilizar esa relación para seleccionar la rama compatible. Si no existe
experiencia diferenciadora, `c`, `g` o `y` permanecen abiertos; repetir una
simetría perfecta no autoriza al runtime a inventar una preferencia.

Los límites entre muestras son fronteras de ejecución, no etiquetas de
segmentación: Aurora no recibe sílabas, palabras ni cortes esperados. Cuando se
necesita que las ventanas compitan a través de todo un flujo, el flujo completo
se entrega como una sola observación, con espacios y signos tratados como
tensores ordinarios.

`corpus_experiment.py` contiene el primer ensayo reproducible. Entrena 12
secuencias españolas durante tres épocas. Ante el texto `luna`, la memoria
vacía mantiene dos ramas empatadas:

```text
lun | a
l | una
```

Después del corpus, `una` posee soporte `24` y la competencia conserva una
sola rama activa para esa consulta. `lun` continúa almacenada: perder la
estructura activa no significa ser eliminada.

## Selección contextual y poda descendente

`context_experiment.py` conserva el ensayo 0.10: demuestra que los cierres
recurrentes pueden seleccionar sentidos de `c`, `g` e `y`. La versión 0.11 usa
esas mismas relaciones como un índice fractal. Cada unidad superior se
descompone por su procedencia hasta encontrar los tensores de carácter que la
originaron; las coincidencias reejecutables restringen las lecturas inferiores
antes de iniciar el ascenso.

Las posiciones unidas por el mismo cierre compiten juntas. Las regiones sin
una relación común forman componentes independientes, evitando construir un
producto global. La prioridad sigue siendo la misma: recurrencia exacta y
anchura comprimida. No hay pesos, umbrales, etiquetas ni comparación textual.

El ensayo usa seis experiencias fonéticas validadas y después consulta seis
flujos sin anotar. Tras cuatro épocas obtiene:

| Consulta sin sentido declarado | Lectura seleccionada | Cierre transferido |
|---|---|---|
| ` cama` | `c=velar` | ` ca` |
| ` cero` | `c=coronal` | ` ce` |
| ` gana` | `g=voiced` | ` ga` |
| ` gesto` | `g=fricative` | ` ge` |
| ` soy ` | `y=vowel` | `oy ` |
| ` ya ` | `y=consonant` | contexto completo |

Antes del aprendizaje, cada consulta conserva dos ganadores. Después, cada
una conserva uno y ejecuta una sola lectura. En el flujo combinado
` cama gesto soy `, tres ambigüedades binarias producen ocho combinaciones
posibles; el descenso activa una y poda siete antes del crecimiento. La ruta
seleccionada coincide con la evaluación exhaustiva de las ocho ramas.

Podar no borra el tensor ni escribe una relación falsa para la rama evitada.
El sentido continúa disponible en el lexicón y puede reabrirse en otro
contexto. Si dos rutas superiores empatan, ambas asignaciones se materializan.

## Módulos

- `aurora.py`: trits, TriGate reversible, ordenación, cara, ventana, tensor
  1–3–9, memoria relacional y reejecución.
- `relational.py`: ejecutor universal dirigido por semillas tensoriales y
  conexiones educativas, sin acciones semánticas especializadas.
- `education_experiment.py`: crecimiento vertical y continuación abierta
  expresados como dos educaciones del mismo runtime.
- `tensor_program.py`: programas de nueve tripletas, reflexión de disparos e
  inducción de código desde procedencia causal.
- `tensor_program_experiment.py`: síntesis y ejecución reproducible de código.
- `provenance_experiment.py`: generación de candidatos desde ejecuciones.
- `fractal_dictionary.py`: promoción `1–3–9` y navegación recursiva mediante
  `C-O`, usando el átomo `DO` del propio programa.
- `fractal_dictionary_experiment.py`: rutas modales, apertura y realimentación
  reproducibles.
- `output_face.py`: búsqueda paralela de tres salidas y escritura conservadora
  de una única ausencia determinada.
- `output_face_experiment.py`: casos `111`, `110`, `100` y `112` con relectura
  del tensor cristalizado.
- `orientation.py`: enlace `O→C`, herencia vertical de `ES` y presentación de
  una misma unidad completa desde sus tres orientaciones.
- `orientation_experiment.py`: auditoría reproducible desde tripleta, SO,
  tensor y ventana hasta el control emergente.
- `deduction.py`: consulta y competencia deductiva de tensores.
- `control.py`: C4–C6, lectura de `HDS/HDE/HDO` y proyección de `Kcontrol`.
- `routing.py`: diccionario distribuido y aprendizaje de rutas entre nodos.
- `tokens.py`: tensores canónicos de tokens simples.
- `characters.py`: tensores fractales 1–3–9 para caracteres.
- `growth.py`: oráculo experimental 0.7–0.11 para cierre, `carry`, recurrencia,
  competencia solapada y ascenso fractal.
- `training.py`: oráculo experimental de observación, selección contextual y
  checkpoints JSON.
- `corpus_experiment.py`: primer entrenamiento reproducible sobre texto real.
- `context_experiment.py`: competencia y transferencia de lecturas de `c/g/y`.
- `downward_experiment.py`: poda descendente y equivalencia con el recorrido
  exhaustivo de lecturas.
- `stream.py`: ensayo léxico secuencial heredado de 0.4.
- `audit.py`: enumeración exhaustiva del perfil finito.

## Ejemplo mínimo

```python
from aurora_compact import aurora, control, deduction, growth, tensor_program, tokens, training
from aurora_compact import context_experiment

packet = aurora.trigate(
    1, 2, 2, r=1, direction=aurora.Direction.DEDUCE_B
)
assert packet.candidates == frozenset({1})

query = deduction.DeductiveQuery.for_tensor((1, 1, 2))
assert query.accepts((1, 1, 0))

operation, coherence, scope = control.interpret(
    (1, 1, 2), (1, 1, 2), (0, 0, 0)
)
assert operation is aurora.Direction.INFER_R
assert scope is control.SearchScope.LOCAL

lexicon = tokens.numeric_lexicon(("cero", "uno", "dos", "tres"))
assert lexicon.lookup("tres")[0].ds == (0, 1, 0)

text = growth.grow_text("aaaaaaaaa")
assert text.growth.complete

a = aurora.Unit.leaf((0, 0, 0))
b = aurora.Unit.leaf((0, 0, 1))
competition = growth.compete_level((a, a, b) * 3)
assert len(competition.candidates) == 7
assert competition.hypothesis_count == 19
assert [(item.start, item.stop) for item in
        competition.selected.segments] == [(0, 3), (3, 6), (6, 9)]

trained = training.train_corpus(("una luna.", "la luna sale."), epochs=2)
assert trained.state.observation_count == 4
assert training.ranked_closures(trained.state)

contextual = context_experiment.run()
probe = training.evaluate_text(contextual.state, " cama")
assert probe.selected.senses == ((1, "velar"),)

program = tensor_program.ProgramTensor.author(
    ((0, 0, 0), (0, 0, 1), (0, 0, 2)),
    ((1, 0, 1), (1, 1, 0), (1, 1, 1)),
    aurora.Direction.INFER_R,
)
assert program.executable
```

## Validar

```bash
python -m unittest discover -s aurora_compact -v
python -m aurora_compact.demo
python -m aurora_compact.experiment
python -m aurora_compact.corpus_experiment
python -m aurora_compact.context_experiment
python -m aurora_compact.downward_experiment
python -m aurora_compact.education_experiment
python -m aurora_compact.tensor_program_experiment
python -m aurora_compact.provenance_experiment
python -m aurora_compact.fractal_dictionary_experiment
python -m aurora_compact.output_face_experiment
python -m aurora_compact.orientation_experiment
python -m aurora_compact.release_candidate_experiment
python -m aurora_compact.audit
```

El candidato contiene 143 pruebas y mantiene el experimento reproducible de
600 secuencias. La auditoría enumera las 243 configuraciones dirigidas del
TriGate y 46.875 caras, ventanas y controles en total: 15.625 por dirección.

## Ejecutor universal, tensor-programa y diccionario 0.12–0.17

Una semilla operativa es una `Unit`. La mayoría de su `DS` determina la
dirección de la cara y su `DO` conserva la fase. La educación enlaza tres
celdas de entrada con tres celdas de salida. El runtime solo ejecuta:

```text
cambio → face() → (DO,DE,DS) → relaciones dependientes
```

El ensayo vertical presenta nueve hojas a tres semillas y vuelve a presentar
sus tres `DS` a una cuarta. Obtiene `9→3→1` sin bucle de niveles. Otro ensayo
produce primero `DE=222` y conecta su `DS` con dos señales posteriores; la
segunda cara alcanza `DE=111` sin una condición programada para `carry`.

Todas las emisiones conservan la procedencia completa y se reejecutan. La
educación puede guardarse como JSON de tensores y conexiones.

La versión 0.13 traslada también las conexiones al vocabulario ternario. Un
programa contiene nueve tripletas: tres direcciones de entrada, tres de salida
y `(DO,DE,DS)`. Presentar `A,A,B` a nueve caras sintetiza un nuevo programa `A`
reejecutable, que se ejecuta sin soporte, contador, peso ni umbral. Si la
síntesis contiene una dirección imposible, las tres candidatas permanecen en
la procedencia y el programa no se activa.

La versión 0.14 conserva además los nueve átomos del programa dentro de cada
semilla ejecutada. Un disparo puede reflejarse de nuevo como `ProgramTensor`
sin llamar a `author()`. Los disparos cuyas tres señales progenitoras poseen la
misma huella causal forman ventanas de experiencia; cada tres programas
reflejados se presentan a las mismas nueve caras de inducción de 0.13.

Así, `A,A,B→A` ya no recibe `A,A,B` como una lista de código escrita por el
anfitrión: recibe tres ejecuciones y recupera los programas desde su propia
procedencia. Ventanas causales diferentes no se mezclan y una síntesis abierta
continúa conservando las tres hipótesis.

La versión 0.15 inserta esos programas reflejados en un bosque ternario. Cada
tres programas producen un nodo y cada tres nodos producen una raíz ejecutable.
La navegación usa `C=0` para aprendizaje, `C=1` para inferencia y deja que el
átomo `DO` determine `O` cuando `C=2` conserva la decisión abierta.

La versión 0.16 presenta tres requisitos de salida al mismo bosque desde los
índices `0`, `1` y `2`. Dos hallazgos determinados autorizan la incorporación
del único tensor ausente; dos ausencias devuelven las salidas sin escribir, y
un `2` conserva abierta la búsqueda. La política está validada, pero su acción
final todavía se orquesta en `output_face.py` y debe migrarse a conexiones del
ejecutor universal.

La versión 0.17 comprueba que la orientación ya forma una cadena única. Una
tripleta satisface `ES=P[O]`; la SO y el tensor-programa comparten exactamente
la misma instrucción `K`; el carry conserva esa unidad completa y sus tres
progenitores; y `HDS/HDE/HDO` se proyectan de nuevo como `Kcontrol`. El mismo
objeto puede presentarse desde `0`, `1` y `2` sin ser reconstruido.

## Frontera del release candidate

Las primitivas finales de control, deducción y red ya son ejecutables. La
realimentación dinámica que debe permitir que `R(HDS)` cambie la dirección de
la siguiente cara y que `R(HDO)` mueva automáticamente una consulta entre
diccionario, red y parada aún no sustituye el ciclo léxico de `transcend()`.
Tampoco se implementa transporte de red real: `routing.py` es una simulación
determinista en memoria para probar la autosimilitud del protocolo.

El crecimiento por `E`, la promoción de cierres recurrentes, la competencia
solapada, el entrenamiento incremental, la selección contextual y la poda
descendente operan en el banco de pruebas heredado. Aún deben migrarse a
semillas tensoriales antes de considerarlos arquitectura final.

La procedencia ya propone los programas que participaron en una ventana, la
promoción ternaria los realimenta y el mismo `K` puede recuperarse desde sus
tres canales. El RC sustituye las cuatro acciones de salida y movimiento por
puertos orientados: la siguiente tarea es aprender las topologías concretas que
conectan esos puertos y conseguir que una contradicción active otra raíz sin
una consulta nueva del anfitrión.

También falta una fuente de experiencia fonética: la ortografía aislada no
contiene por sí sola toda la pronunciación. Un cierre estructural no se etiqueta
automáticamente como «sílaba». `growth.py` permanece únicamente como oráculo
histórico para contrastar esas educaciones futuras.

## Licencia y procedencia

Implementación derivada del Proyecto Aurora. Código bajo Apache 2.0 y
documentación bajo CC BY 4.0, conforme a los avisos del material de origen.
