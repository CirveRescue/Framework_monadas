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