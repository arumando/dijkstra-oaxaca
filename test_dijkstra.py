"""Pruebas del algoritmo de Dijkstra. Ejecutar con: python -m unittest"""

import tempfile
import unittest
from pathlib import Path

from dijkstra import INFINITO, DatosIncompletos, cargar_grafo, dijkstra, ruta_mas_corta

DATOS = Path(__file__).parent / "datos"


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.grafo = cargar_grafo(DATOS / "ejemplo_didactico.csv")

    def test_grafo_es_no_dirigido(self):
        self.assertEqual(self.grafo["A"]["B"], self.grafo["B"]["A"])

    def test_ruta_mas_corta(self):
        distancia, camino = ruta_mas_corta(self.grafo, "A", "F")
        self.assertEqual(distancia, 9)
        self.assertEqual(camino, ["A", "C", "B", "D", "F"])

    def test_distancias_desde_origen(self):
        distancias, _ = dijkstra(self.grafo, "A")
        self.assertEqual(distancias, {"A": 0, "B": 4, "C": 3, "D": 6, "E": 10, "F": 9})

    def test_origen_igual_a_destino(self):
        self.assertEqual(ruta_mas_corta(self.grafo, "C", "C"), (0, ["C"]))

    def test_localidad_inexistente(self):
        with self.assertRaises(KeyError):
            ruta_mas_corta(self.grafo, "A", "Z")

    def test_sin_camino(self):
        grafo = {"A": {"B": 1}, "B": {"A": 1}, "X": {}}
        self.assertEqual(ruta_mas_corta(grafo, "A", "X"), (INFINITO, []))

    def test_distancias_pendientes(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "rutas.csv"
            ruta.write_text("origen,destino,distancia_km\nA,B,PENDIENTE\n", encoding="utf-8")
            with self.assertRaises(DatosIncompletos):
                cargar_grafo(ruta)


if __name__ == "__main__":
    unittest.main()
