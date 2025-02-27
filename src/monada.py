class Monada:
    def __init__(self, value):
        self.value = value

    def bind(self, func):
        """
        Encadena una operación sobre el valor encapsulado.
        """
        try:
            result = func(self.value)
            return result
        except Exception as e:
            print(f"Error en bind: {e}")
            return Monada([])  # Devuelve una lista vacía en caso de error

    def map(self, func):
        """
        Aplica una función al valor encapsulado (functor).
        """
        return self.bind(lambda x: Monada(func(x)))

    def apply(self, other_monada):
        """
        Aplica una función encapsulada a otro valor encapsulado (aplicativo).
        """
        return self.bind(lambda f: other_monada.map(f))

    def __repr__(self):
        return f"Monada({self.value})"