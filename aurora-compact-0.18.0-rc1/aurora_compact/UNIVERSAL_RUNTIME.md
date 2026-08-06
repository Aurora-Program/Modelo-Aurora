# Del simulador al ejecutor universal

Aurora compacto 0.12 conserva las capas 0.7–0.11 como banco de pruebas, pero
deja de tratarlas como arquitectura definitiva. Esas capas demostraron que el
nucleo puede sostener crecimiento, competencia y selección; también hicieron
visible que parte de ese comportamiento estaba decidido por código externo.

La nueva rama reduce el runtime a una sola transición:

```text
cambio de celda
→ presentar tres señales
→ ejecutar una cara
→ publicar (DO,DE,DS)
→ reactivar relaciones dependientes
```

## Qué pertenece al runtime

- Detectar que una celda recibió una señal nueva.
- Reunir las tres celdas declaradas por una semilla.
- Leer `C` y la fase desde el tensor de esa semilla.
- Ejecutar la cara congelada.
- Publicar los tres canales sin interpretarlos.
- Preservar alternativas y procedencia.
- Detenerse en un punto fijo o al agotar el gasto.

## Qué pertenece a la educación

- Qué tres unidades deben presentarse juntas.
- Qué salida se presenta a qué relación posterior.
- Qué dirección utiliza cada semilla.
- Qué ramas superiores vuelven a activar ramas inferiores.
- Qué organizaciones abiertas reciben contexto nuevo.

La educación es un documento de tensores y conexiones. No contiene callbacks,
clasificadores ni nombres de operaciones lingüísticas.

## Dos equivalencias ya ejecutadas

### Crecimiento vertical

Nueve señales se presentan a tres semillas inferiores. Sus tres salidas `DS`
se presentan a una cuarta semilla. El ejecutor realiza cuatro disparos y
obtiene una raíz de profundidad dos:

```text
9 entradas → 3 caras → 1 cara
```

No existe `grow_fractal()`, contador de nivel ni llamada a `ascend()` en este
camino.

### Continuación de una apertura

La primera presentación produce `DE=222`. Su `DS` se presenta, por educación,
con las dos señales siguientes. La segunda cara produce `DE=111`.

No existe una rama `if DE == 222`, ni un objeto `Carry`, ni una acción especial
para continuar. El nombre *carry* describe desde fuera el efecto de la
conexión educativa.

## Límite del perfil 0.12

Aurora todavía no ha aprendido estas conexiones: se las hemos presentado como
educación inicial. El siguiente experimento debe representar la propia
creación y estabilización de una conexión como relaciones Aurora competidoras.
Solo entonces la recurrencia dejará de ser un contador externo y pasará a ser
conocimiento ternario operativo.

## Extensión 0.13: la presentación también es tensor

El perfil 0.13 codifica tres entradas, tres salidas y `(DO,DE,DS)` en nueve
tripletas. El ejecutor 0.12 permanece igual: un compilador mecánico transforma
esas direcciones ternarias en referencias de celda y entrega la instrucción a
la misma propagación por eventos.

Tres programas completos pueden presentarse, posición por posición, a nueve
caras. Dos programas coincidentes y una alternativa sintetizan un programa
reejecutable; una dirección literal imposible mantiene la síntesis abierta y
evita su ejecución. La educación todavía presenta las candidatas: generarlas
desde la procedencia de una ventana es la siguiente frontera.

## Extensión 0.14: la ejecución conserva el programa

Cada semilla compilada conserva las nueve unidades educativas que la
originaron. Un disparo puede reflejarlas de nuevo como `ProgramTensor` y
verificar que coinciden con la ruta realmente ejecutada. Tres disparos de la
misma ventana causal presentan así sus propios programas a las nueve caras de
inducción; el anfitrión ya no redacta la lista de candidatas.

## Extensión 0.15: el diccionario se orienta con C-O

Los programas reflejados entran en un bosque ternario. Cada terna se sintetiza
como programa del nivel siguiente; nueve experiencias pueden formar así una
raíz reejecutable sin un controlador de ascenso. `C=0` y `C=1` recorren sus
ramas determinadas. `C=2` conserva apertura y usa la ordenación del átomo `DO`.
Si ese orden también permanece abierto, todas las alternativas se conservan.

La frontera actual es conectar varias familias `DS` y realimentar una
contradicción hasta otra raíz sin una nueva consulta del anfitrión.

## Extensión 0.16: la salida consulta y escribe

Los tres tensores de salida consultan el bosque desde sus índices `0`, `1` y
`2`. Las respuestas forman una tripleta ternaria: `1` encontrado, `0` ausente
y `2` todavía abierto. `111` continúa; una mayoría con un único `0` incorpora
solo el tensor ausente; una mayoría `0` devuelve las salidas; cualquier `2`
conserva las alternativas.

La unidad escrita debe existir ya como salida causal ejecutable. La consulta no
autora un programa ni escribe dos incógnitas para forzar un cierre. Esta
política todavía se orquesta en `output_face.py`; migrar sus cuatro resultados
a conexiones educativas es la siguiente frontera del ejecutor universal.
