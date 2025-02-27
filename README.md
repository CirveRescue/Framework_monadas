# Framework de Procesamiento de Flujos de Datos Basado en Mónadas

Este proyecto es un framework de procesamiento de flujos de datos en Python que utiliza conceptos avanzados de programación funcional, como **mónadas**, **functores** y **aplicativos**. El framework permite manipular flujos de datos de manera asíncrona, funcional y sin efectos secundarios.

## Características Principales

- **Mónadas**: Implementación de una clase `Monada` que encapsula valores y permite operaciones como `bind`, `map`, y `apply`.
- **Functores y Aplicativos**: Extensión de la clase `Monada` para soportar las interfaces de functor y aplicativo.
- **Funciones Utilitarias**: Funciones como `map_ofertas`, `filter_ofertas`, y `reducir_ofertas` para manipular listas de datos.
- **Manejo de Errores**: Sistema básico de manejo de errores dentro del framework.
- **Aplicación de Ejemplo**: Un scraper de ofertas de MercadoLibre que utiliza el framework para extraer, procesar y enviar ofertas a Telegram.

---

## Estructura del Proyecto

El proyecto está organizado en los siguientes módulos:

1. **`monada.py`**: Implementa la clase `Monada` y sus métodos principales.
2. **`scraper.py`**: Contiene funciones asíncronas para extraer ofertas de MercadoLibre.
3. **`utils.py`**: Proporciona funciones utilitarias para manipular listas de ofertas.
4. **`main.py`**: Es el punto de entrada del programa, donde se coordina la extracción, procesamiento y envío de ofertas a Telegram.

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
3. Ejecuta el proyecto:
   ```bash
   python main.py

   ### 1. Investigación y Documentación

#### Conceptos de Mónadas, Functores y Aplicativos

En programación funcional, los conceptos de **mónadas**, **functores** y **aplicativos** son fundamentales para manejar efectos secundarios, manipular datos encapsulados y componer operaciones de manera segura y estructurada. A continuación, se explican estos conceptos y cómo se implementan en Python utilizando el código proporcionado.

---

#### **Functores**

Un **functor** es una estructura que encapsula un valor y permite aplicar una función a ese valor sin desencapsularlo. En términos simples, un functor es cualquier tipo que implementa una operación `map`, que toma una función y la aplica al valor encapsulado.

**Ejemplo en Python:**

En el código, la clase `Monada` implementa un functor a través del método `map`. Este método toma una función y la aplica al valor encapsulado, devolviendo una nueva instancia de `Monada` con el resultado.

```python
class Monada:
    def __init__(self, value):
        self.value = value

    def map(self, func):
        """
        Aplica una función al valor encapsulado (functor).
        """
        return self.bind(lambda x: Monada(func(x)))
```

**Uso en el código:**

En `main.py`, se utiliza `map` para formatear los precios de las ofertas:

```python
monada_ofertas = monada_ofertas.map(
    lambda ofertas: map_ofertas(ofertas, lambda o: {**o, 'precio_actual': float(o['precio_actual'].replace('$', '').replace(',', ''))})
)
```

Aquí, `map` aplica una función que convierte el precio actual de una cadena a un número flotante.

---

#### **Aplicativos**

Un **aplicativo** es un functor que permite aplicar una función encapsulada a otro valor encapsulado. En otras palabras, un aplicativo permite trabajar con funciones que también están encapsuladas.

**Ejemplo en Python:**

La clase `Monada` implementa la operación `apply`, que toma otra `Monada` que contiene una función y la aplica al valor encapsulado.

```python
class Monada:
    def apply(self, other_monada):
        """
        Aplica una función encapsulada a otro valor encapsulado (aplicativo).
        """
        return self.bind(lambda f: other_monada.map(f))
```

**Uso en el código:**

Aunque no se usa directamente en el código proporcionado, `apply` podría usarse para aplicar una función encapsulada a una lista de ofertas encapsuladas.

---

#### **Mónadas**

Una **mónada** es una estructura que encapsula un valor y permite encadenar operaciones sobre ese valor utilizando `bind` (también conocido como `flatMap`). Las mónadas son útiles para manejar efectos secundarios, como la manipulación de datos asíncronos o el manejo de errores.

**Ejemplo en Python:**

La clase `Monada` implementa la operación `bind`, que toma una función que devuelve otra `Monada` y la aplica al valor encapsulado.

```python
class Monada:
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
```

**Uso en el código:**

En `main.py`, `bind` se utiliza para filtrar las ofertas que tienen un descuento del 50% o más:

```python
monada_ofertas = monada_ofertas.bind(
    lambda ofertas: Monada(filter_ofertas(ofertas, lambda o: o['descuento'] >= 50))
)
```

Aquí, `bind` toma una función que filtra las ofertas y devuelve una nueva `Monada` con las ofertas filtradas.

---

#### **Relación entre Functores, Aplicativos y Mónadas**

- **Functores**: Permiten aplicar una función a un valor encapsulado.
- **Aplicativos**: Permiten aplicar una función encapsulada a un valor encapsulado.
- **Mónadas**: Permiten encadenar operaciones que devuelven valores encapsulados.

En el código proporcionado, la clase `Monada` implementa los tres conceptos:
- `map` para functores.
- `apply` para aplicativos.
- `bind` para mónadas.

---

#### **Implementación en el Código**

El código utiliza estas estructuras para manipular las ofertas extraídas de MercadoLibre:

1. **Extracción de ofertas**: Las ofertas se extraen de manera asíncrona y se encapsulan en una `Monada`.
2. **Formateo y filtrado**: Se utilizan `map` y `bind` para formatear precios, limpiar descuentos y filtrar ofertas.
3. **Envío a Telegram**: Las ofertas procesadas se envían a un chat de Telegram en lotes.

**Ejemplo completo:**

```python
# Encapsular las ofertas en una monada
monada_ofertas = Monada(todas_las_ofertas)

# Formatear precios antes de filtrar
monada_ofertas = monada_ofertas.map(
    lambda ofertas: map_ofertas(ofertas, lambda o: {**o, 'precio_actual': float(o['precio_actual'].replace('$', '').replace(',', ''))})
)

# Limpiar y normalizar el campo descuento
monada_ofertas = monada_ofertas.map(
    lambda ofertas: map_ofertas(ofertas, lambda o: {**o, 'descuento': limpiar_descuento(o['descuento'])})
)

# Filtrar ofertas con al menos 50% de descuento
monada_ofertas = monada_ofertas.bind(
    lambda ofertas: Monada(filter_ofertas(ofertas, lambda o: o['descuento'] >= 50))
)

# Formatear precios para mostrar
monada_ofertas = monada_ofertas.map(
    lambda ofertas: map_ofertas(ofertas, lambda o: {**o, 'precio_actual': f"${o['precio_actual']:.2f}"} )
)

# Acortar las URLs de las ofertas
monada_ofertas = monada_ofertas.map(
    lambda ofertas: map_ofertas(ofertas, lambda o: {**o, 'url': acortar_url(o['url'])})
)
```

---

#### **Conclusión**

El uso de mónadas, functores y aplicativos en este proyecto permite manipular las ofertas de manera segura y estructurada, evitando efectos secundarios y facilitando la composición de operaciones. Este enfoque funcional es especialmente útil en proyectos donde se requiere claridad y mantenibilidad en el manejo de datos.

--- 


