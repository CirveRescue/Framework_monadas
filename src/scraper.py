import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def extraer_ofertas_pagina(session, url, pagina):
    """
    Extrae las ofertas de una página específica de manera asíncrona.
    """
    try:
        # Añadir el número de página a la URL
        url_pagina = f"{url}?page={pagina}" if pagina > 1 else url

        # Hacer la solicitud HTTP asíncrona
        async with session.get(url_pagina) as response:
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            html = await response.text()

        # Parsear el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Lista para almacenar las ofertas
        ofertas = []

        # Buscar todos los divs que contienen las ofertas
        for item in soup.find_all('div', class_='andes-card'):
            # Extraer el título y la URL
            titulo_tag = item.find('a', class_='poly-component__title')
            titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
            url_oferta = titulo_tag['href'] if titulo_tag and 'href' in titulo_tag.attrs else url_pagina

            # Extraer el precio actual desde el contenedor correcto
            precio_actual_container = item.find('div', class_='poly-price__current')
            if precio_actual_container:
                precio_actual = precio_actual_container.find('span', class_='andes-money-amount__fraction')
                precio_actual = precio_actual.text.strip() if precio_actual else "0"
            else:
                precio_actual = "0"  # Si no hay precio actual, usar "0"

            # Extraer el precio anterior (tachado)
            precio_anterior = item.find('s', class_='andes-money-amount--previous')
            precio_anterior = precio_anterior.find('span', class_='andes-money-amount__fraction').text.strip() if precio_anterior else "0"

            # Extraer el descuento
            descuento = item.find('span', class_='andes-money-amount__discount')
            descuento = descuento.text.strip() if descuento else "0%"

            # Extraer información de envío
            envio = item.find('div', class_='poly-component__shipping')
            envio = envio.text.strip() if envio else "Sin envío gratis"

            # Añadir la oferta a la lista
            ofertas.append({
                "titulo": titulo,
                "precio_actual": precio_actual,  # Mantenemos como cadena (str)
                "precio_anterior": precio_anterior,
                "descuento": descuento,
                "envio": envio,
                "url": url_oferta  # Usamos la URL de la etiqueta <a>
            })

        return ofertas

    except Exception as e:
        print(f"Error al acceder a {url_pagina}: {e}")
        return []  # Devuelve una lista vacía en caso de error

async def extraer_todas_las_ofertas(url):
    """
    Recorre todas las páginas y extrae las ofertas de manera asíncrona.
    """
    # Crear una sesión asíncrona
    async with aiohttp.ClientSession() as session:
        # Extraer el número total de páginas
        total_paginas = await extraer_total_paginas(session, url)
        print(f"Total de páginas detectadas: {total_paginas}")

        # Crear una lista de tareas para extraer ofertas de cada página
        tareas = [extraer_ofertas_pagina(session, url, pagina) for pagina in range(1, total_paginas + 1)]

        # Ejecutar todas las tareas en paralelo
        resultados = await asyncio.gather(*tareas)

        # Combinar los resultados de todas las páginas
        todas_las_ofertas = [oferta for sublist in resultados for oferta in sublist]
        return todas_las_ofertas

async def extraer_total_paginas(session, url):
    """
    Extrae el número total de páginas desde la paginación.
    """
    try:
        # Hacer la solicitud HTTP asíncrona
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()

        # Parsear el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Buscar la paginación
        paginacion = soup.find('ul', class_='andes-pagination')
        if not paginacion:
            return 1  # Si no hay paginación, asumimos que solo hay una página

        # Extraer todos los enlaces de paginación
        paginas = paginacion.find_all('li', class_='andes-pagination__button')
        if not paginas:
            return 1  # Si no hay botones de paginación, asumimos que solo hay una página

        # Obtener el número de la última página
        ultima_pagina = None
        for pagina in paginas:
            enlace = pagina.find('a', class_='andes-pagination__link')
            if enlace and enlace.text.isdigit():  # Solo considerar enlaces con números
                ultima_pagina = enlace

        if not ultima_pagina:
            return 1  # Si no hay enlace con número, asumimos que solo hay una página

        # Extraer el número de la última página
        return int(ultima_pagina.text)

    except Exception as e:
        print(f"Error al extraer el total de páginas: {e}")
        return 1  # En caso de error, asumimos que solo hay una página