# La cara de salida lee y escribe

Aurora compacto 0.16 prueba la regla ternaria de lectura y escritura propuesta
para la cara de salida. No existe una consulta única para toda la salida. Sus
tres tensores consultan el mismo bosque fractal en paralelo y cada uno entra
por su propio índice operativo:

```text
salida 0 → C=0
salida 1 → C=1
salida 2 → C=2 → O cuando la decisión permanece abierta
```

Cada consulta produce un trit de hallazgo:

| Trit | Estado de la búsqueda |
|---:|---|
| `0` | el recorrido determinado terminó sin encontrar el tensor requerido |
| `1` | el tensor requerido fue encontrado y puede reejecutarse |
| `2` | el orden todavía no determina una rama; se conservan las alternativas |

La cara obtiene así una tripleta `H=(h0,h1,h2)`. Si existe un `2`, la
operación no convierte la apertura en ausencia ni escribe conocimiento. Cuando
los tres estados están determinados, la misma mayoría ternaria decide si hay
base suficiente para avanzar.

## Tres cierres: continuar

```text
H=111 → reutilizar → continuar
```

Los tres tensores ya existen en el diccionario y han vuelto a cerrar desde sus
índices. La memoria no cambia.

## Dos cierres: cristalizar solo el ausente

```text
H=110 → escribir salida 2 → releer → 111 → continuar
H=101 → escribir salida 1 → releer → 111 → continuar
H=011 → escribir salida 0 → releer → 111 → continuar
```

La escritura no autoriza a fabricar un programa. Inserta exactamente el tensor
de salida que la ejecución ya produjo. Ese tensor debe conservar sus nueve
unidades, poder reejecutarse y contener una instrucción cerrada. Si no cumple
esas condiciones, la ruta devuelve las salidas y el diccionario permanece
intacto.

La prueba principal parte de dos hallazgos y un programa recuperado de un
disparo causal real. Después de insertarlo, el mismo diccionario lo encuentra
desde el índice que antes respondió `0`.

## Cero o un cierre: devolver la salida

```text
H=100 → camino imposible → devolver tres salidas
H=000 → camino imposible → devolver tres salidas
```

Con dos ausencias no existe mayoría que determine qué dos relaciones deberían
crearse. Aurora conserva los tensores de salida y no modifica la memoria.

## La apertura sigue siendo apertura

```text
H=112 → conservar alternativas → esperar orientación
```

Aunque dos ramas hayan cerrado, el tercer `2` no equivale a un tensor ausente.
En el experimento conserva los nueve descendientes del nodo abierto y no
cristaliza nada.

## Escritura dentro del bosque

El diccionario de 0.15 solo permitía consultar cuando toda su frontera era una
única raíz. La nueva búsqueda recorre primero los niveles estructurales más
altos y después las fronteras causales todavía no promovidas. Así, después de
añadir una décima unidad, la raíz de nueve hojas permanece disponible y la
nueva hoja puede releerse inmediatamente:

```text
niveles antes   = [0,0,1]
niveles después = [1,0,1]
```

No se reconstruye ni se reordena la raíz anterior. Cuando tres hojas nuevas se
acumulen, formarán otro nodo mediante la promoción ternaria ya existente.

## Límite exacto

0.16 valida la política de mayoría, la consulta paralela, la apertura y la
escritura conservadora sobre programas tensoriales. `output_face.py` todavía
orquesta la acción final en Python. La siguiente migración rigurosa consiste en
representar también `continuar`, `cristalizar`, `devolver` y `esperar` como
salidas conectadas de semillas ordinarias del ejecutor relacional.
