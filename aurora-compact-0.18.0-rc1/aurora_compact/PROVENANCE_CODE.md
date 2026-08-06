# El código nace de la procedencia

Aurora compacto 0.14 elimina la concesión principal de 0.13: el anfitrión ya
no entrega directamente tres `ProgramTensor` a la competencia. Las propias
ejecuciones conservan los nueve átomos tensoriales del programa que las
produjo y pueden volver a presentarlos a las mismas nueve caras de inducción.

El ciclo demostrado es:

```text
programa tensorial
→ ejecución
→ disparo con procedencia
→ reflexión del programa
→ ventana de tres experiencias
→ nueve caras
→ nuevo programa tensorial
→ ejecución
```

## Procedencia educativa

Cada `OperationalSeed` conserva dos elementos distintos:

- el tensor de instrucción que determina fase y dirección;
- las unidades educativas reejecutables que dieron forma al programa.

Para un programa completo son nueve unidades:

```text
(I0,I1,I2) | (ODO,ODE,ODS) | (DO,DE,DS)
```

La ejecución no interpreta esas unidades. Solo las transporta como parte de
la procedencia causal. El documento JSON de educación también las conserva,
incluidos sus descendientes, por lo que un programa aprendido no se aplana al
guardarse o ejecutarse.

## Reflexión sin autoría externa

`ProgramTensor.from_firing()` reconstruye el programa del disparo verificando
cuatro identidades exactas:

1. existen nueve unidades educativas;
2. todas se reejecutan;
3. sus seis direcciones coinciden con las celdas realmente usadas;
4. `(DO,DE,DS)` coincide con la instrucción realmente ejecutada.

No se calcula una topología nueva mediante etiquetas ni se llama a
`ProgramTensor.author()`. El programa candidato es el mismo código tensorial
que ya participó en la experiencia.

## La ventana causal

Dos disparos pertenecen a la misma ventana únicamente cuando coinciden las
huellas completas de sus tres señales de entrada. La comparación incluye
valor, origen y toda la cadena causal; compartir solo `DS` no basta.

Las experiencias de una misma ventana se conservan en orden. Cada tres
reflexiones consecutivas ocupan una ventana ordinaria y sus nueve posiciones
se presentan a `induce()`:

```text
experiencia A, experiencia A, experiencia B
→ programa A
```

El anfitrión aporta el flujo de experiencias, pero no redacta la lista de
programas candidatos ni les asigna soporte, frecuencia, peso o umbral.

## Pruebas negativas

- Dos experiencias de una ventana y una de otra no forman una competencia.
- Tres programas incompatibles producen la dirección imposible `102`; las
  tres procedencias se conservan y el programa no se ejecuta.
- Un programa emergente puede ejecutarse, reflejarse y serializarse sin perder
  los tres hijos de cada uno de sus nueve átomos.

## Qué demuestra 0.14

Aurora ya puede convertir experiencia causal en candidatos de código, hacerlos
competir y ejecutar el programa que emerge, sin que Python vuelva a escribir
esas candidatas.

La afirmación debe mantenerse precisa: 0.14 propone programas que ya se han
manifestado en una ejecución. El perfil 0.15 incorpora esos programas a un
diccionario ternario: cada tres forman un nodo y cada tres nodos forman una raíz
ejecutable. La posición `DO` de ese mismo código orienta la navegación mediante
`C-O`. Véase `FRACTAL_DICTIONARY.md`.
