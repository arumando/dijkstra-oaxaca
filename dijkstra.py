"""Ruta más corta entre localidades con el algoritmo de Dijkstra.

El mapa se lee de un CSV con columnas: origen,destino,distancia_km
Las carreteras se consideran de doble sentido. Las líneas que empiezan
con '#' son comentarios.

Uso:
    python dijkstra.py "Oaxaca de Juárez" "Ixtlán de Juárez"
    python dijkstra.py A F --datos datos/ejemplo_didactico.csv
    python dijkstra.py --listar
"""

import argparse
import csv
import heapq
import sys
from pathlib import Path

DATOS_POR_DEFECTO = Path(__file__).parent / "datos" / "rutas_oaxaca.csv"
INFINITO = float("inf")


class DatosIncompletos(Exception):
    """Se lanza cuando el CSV tiene distancias marcadas como PENDIENTE."""


def cargar_grafo(ruta: Path) -> dict[str, dict[str, float]]:
    """Lee el CSV y devuelve una lista de adyacencia: {localidad: {vecina: km}}."""
    grafo: dict[str, dict[str, float]] = {}
    pendientes = []

    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        lineas = (l for l in archivo if l.strip() and not l.lstrip().startswith("#"))
        for fila in csv.DictReader(lineas):
            origen = fila["origen"].strip()
            destino = fila["destino"].strip()
            valor = fila["distancia_km"].strip()

            if valor.upper() == "PENDIENTE":
                pendientes.append(f"{origen} - {destino}")
                continue

            distancia = float(valor)
            if distancia <= 0:
                raise ValueError(f"Distancia inválida entre {origen} y {destino}: {valor}")

            grafo.setdefault(origen, {})[destino] = distancia
            grafo.setdefault(destino, {})[origen] = distancia

    if pendientes:
        raise DatosIncompletos(
            f"Faltan {len(pendientes)} distancias en {ruta.name}:\n  "
            + "\n  ".join(pendientes)
        )
    return grafo


def dijkstra(grafo: dict[str, dict[str, float]], origen: str):
    """Calcula la distancia mínima desde `origen` hacia todas las localidades.

    Devuelve (distancias, previo), donde previo[x] es la localidad anterior
    a x en la ruta más corta. Usa una cola de prioridad (heap), por lo que
    su complejidad es O((V + E) log V).
    """
    distancias = {nodo: INFINITO for nodo in grafo}
    previo: dict[str, str | None] = {nodo: None for nodo in grafo}
    distancias[origen] = 0
    cola = [(0, origen)]
    visitados = set()

    while cola:
        distancia_actual, actual = heapq.heappop(cola)
        if actual in visitados:
            continue  # entrada vieja de la cola, ya se procesó con menor distancia
        visitados.add(actual)

        for vecino, peso in grafo[actual].items():
            nueva = distancia_actual + peso
            if nueva < distancias[vecino]:
                distancias[vecino] = nueva
                previo[vecino] = actual
                heapq.heappush(cola, (nueva, vecino))

    return distancias, previo


def ruta_mas_corta(grafo, origen: str, destino: str) -> tuple[float, list[str]]:
    """Devuelve (distancia_total, [origen, ..., destino]).

    Si no hay camino, devuelve (inf, []).
    """
    for nodo in (origen, destino):
        if nodo not in grafo:
            raise KeyError(nodo)

    distancias, previo = dijkstra(grafo, origen)
    if distancias[destino] == INFINITO:
        return INFINITO, []

    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = previo[nodo]
    return distancias[destino], camino[::-1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Ruta más corta entre localidades (Dijkstra).")
    parser.add_argument("origen", nargs="?", help="Localidad de salida")
    parser.add_argument("destino", nargs="?", help="Localidad de llegada")
    parser.add_argument("--datos", type=Path, default=DATOS_POR_DEFECTO,
                        help="CSV con las conexiones (por defecto: datos/rutas_oaxaca.csv)")
    parser.add_argument("--listar", action="store_true", help="Muestra las localidades disponibles")
    args = parser.parse_args()

    try:
        grafo = cargar_grafo(args.datos)
    except DatosIncompletos as error:
        print(f"Error: {error}", file=sys.stderr)
        print("\nCompleta las distancias en el CSV o prueba con:", file=sys.stderr)
        print("  python dijkstra.py A F --datos datos/ejemplo_didactico.csv", file=sys.stderr)
        return 1

    if args.listar or not (args.origen and args.destino):
        print("Localidades disponibles:")
        for nodo in sorted(grafo):
            print(f"  - {nodo}")
        return 0

    try:
        distancia, camino = ruta_mas_corta(grafo, args.origen, args.destino)
    except KeyError as error:
        print(f"Error: la localidad {error} no existe. Usa --listar para ver las opciones.",
              file=sys.stderr)
        return 1

    if not camino:
        print(f"No hay ruta entre {args.origen} y {args.destino}.")
        return 0

    print(f"Ruta más corta de {args.origen} a {args.destino}:")
    for paso, (a, b) in enumerate(zip(camino, camino[1:]), start=1):
        print(f"  {paso}. {a} -> {b}  ({grafo[a][b]:g} km)")
    print(f"Distancia total: {distancia:g} km")
    return 0


if __name__ == "__main__":
    sys.exit(main())
