# 🗺️ Dijkstra aplicado a Oaxaca: ruta más corta entre localidades

Implementación en Python del **algoritmo de Dijkstra** para encontrar la **ruta más corta por carretera** entre localidades de Oaxaca (por ejemplo, de Oaxaca de Juárez a Ixtlán de Juárez, donde está la UNSIJ). El mapa es un **grafo ponderado** que se carga desde un archivo CSV.

> Contexto: [PENDIENTE: materia y semestre en que hiciste este proyecto por primera vez]

## ✨ Qué hace

- Lee el mapa desde un CSV (`origen,destino,distancia_km`): es fácil agregar localidades sin tocar el código.
- Calcula la ruta más corta con **Dijkstra + cola de prioridad** (`heapq`), con complejidad O((V + E) log V).
- Muestra la ruta **paso a paso** y la distancia total.
- Valida los datos: localidades inexistentes, distancias negativas, destinos sin camino y **distancias pendientes**.

```
$ python dijkstra.py A F --datos datos/ejemplo_didactico.csv
Ruta más corta de A a F:
  1. A -> C  (3 km)
  2. C -> B  (1 km)
  3. B -> D  (2 km)
  4. D -> F  (3 km)
Distancia total: 9 km
```

## ⚠️ Estado de los datos

El archivo [`datos/rutas_oaxaca.csv`](datos/rutas_oaxaca.csv) contiene las conexiones entre localidades, pero las **distancias están como `PENDIENTE`**: hay que verificarlas y capturar los kilómetros reales. Mientras falten, el programa avisa cuáles son y no calcula rutas.

Para probar el algoritmo mientras tanto, usa el grafo didáctico [`datos/ejemplo_didactico.csv`](datos/ejemplo_didactico.csv).

## 🛠️ Tecnologías

- Python 3.10+
- Solo biblioteca estándar: `heapq`, `csv`, `argparse`, `pathlib`
- Pruebas con `unittest`

## ▶️ Cómo ejecutarlo

```bash
git clone https://github.com/arumando/dijkstra-oaxaca.git
cd dijkstra-oaxaca

# Ver las localidades disponibles
python dijkstra.py --listar

# Ruta más corta entre dos localidades (usa comillas si el nombre tiene espacios)
python dijkstra.py "Oaxaca de Juárez" "Ixtlán de Juárez"

# Probar con el grafo de ejemplo
python dijkstra.py A F --datos datos/ejemplo_didactico.csv

# Ejecutar las pruebas
python -m unittest -v
```

## 🧠 Cómo funciona Dijkstra (resumen)

1. La distancia al origen es 0 y a todas las demás localidades es infinito.
2. Se toma de la cola de prioridad la localidad **no visitada con menor distancia**.
3. Para cada vecina, si pasar por la localidad actual da una distancia menor, se actualiza la distancia y se guarda de dónde se llegó (`previo`).
4. Se repite hasta visitar todas. La ruta se reconstruye siguiendo `previo` desde el destino hacia atrás.

## 📸 Capturas

[PENDIENTE: captura de la terminal mostrando una ruta calculada]

[PENDIENTE: imagen del grafo o mapa de las localidades]

## 📚 Qué aprendí

<!-- Revisa esta lista y escríbela con tus propias palabras. -->
- Representar un mapa real como un grafo ponderado con listas de adyacencia (diccionarios).
- Implementar Dijkstra con una cola de prioridad y reconstruir el camino más corto.
- Separar los datos (CSV) del algoritmo para poder cambiar el mapa sin tocar el código.
- Probar casos límite: sin camino, origen igual a destino, localidades que no existen.

## 🚀 Posibles mejoras

- Completar las distancias reales y agregar más localidades de la Sierra Juárez.
- Dibujar el grafo y la ruta encontrada con `networkx` y `matplotlib`.
- Considerar el tiempo de viaje además de la distancia.

## 👤 Autor

**José Armando García Bandera** — [github.com/arumando](https://github.com/arumando)
