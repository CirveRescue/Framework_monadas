import unittest
from src.monada import Monada
from src.utils import map_ofertas, filter_ofertas

class TestFramework(unittest.TestCase):
    # Pruebas para la clase Monada
    def test_monad_bind(self):
        """Prueba el método bind de la clase Monada."""
        monada = Monada(5)
        result = monada.bind(lambda x: Monada(x * 2))
        self.assertEqual(result.value, 10)

    def test_monad_map(self):
        """Prueba el método map de la clase Monada."""
        monada = Monada(5)
        result = monada.map(lambda x: x * 2)
        self.assertEqual(result.value, 10)

    def test_monad_apply(self):
        """Prueba el método apply de la clase Monada."""
        monada_func = Monada(lambda x: x + 1)
        monada_valor = Monada(5)
        result = monada_func.apply(monada_valor)
        self.assertEqual(result.value, 6)

    def test_monad_bind_error(self):
        """Prueba el manejo de errores en el método bind."""
        monada = Monada(5)
        result = monada.bind(lambda x: Monada(x / 0))  # División por cero
        self.assertEqual(result.value, [])  # Verifica que se maneje el error correctamente

    # Pruebas para las funciones utilitarias
    def test_map_ofertas(self):
        """Prueba la función map_ofertas."""
        ofertas = [{"precio_actual": 30}, {"precio_actual": 60}]
        result = map_ofertas(ofertas, lambda o: {"precio_actual": o['precio_actual'] * 2})
        self.assertEqual(result[0]['precio_actual'], 60)
        self.assertEqual(result[1]['precio_actual'], 120)

    def test_filter_ofertas(self):
        """Prueba la función filter_ofertas."""
        ofertas = [{"precio_actual": 30}, {"precio_actual": 60}]
        filtradas = filter_ofertas(ofertas, lambda o: o['precio_actual'] < 50)
        self.assertEqual(len(filtradas), 1)
        self.assertEqual(filtradas[0]['precio_actual'], 30)

    def test_filter_ofertas_vacias(self):
        """Prueba la función filter_ofertas con una lista vacía."""
        ofertas = []
        filtradas = filter_ofertas(ofertas, lambda o: o['precio_actual'] < 50)
        self.assertEqual(len(filtradas), 0)

    def test_filter_ofertas_invalidas(self):
        """Prueba la función filter_ofertas con datos inválidos."""
        ofertas = [{"precio_actual": "treinta"}, {"precio_actual": 60}]
        filtradas = filter_ofertas(ofertas, lambda o: isinstance(o['precio_actual'], int) and o['precio_actual'] < 50)
        self.assertEqual(len(filtradas), 0)

if __name__ == "__main__":
    unittest.main()