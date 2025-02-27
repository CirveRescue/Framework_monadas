import asyncio
import requests
import os
from src.scraper import extraer_todas_las_ofertas
from src.monada import Monada
from src.utils import map_ofertas, filter_ofertas

# Configuración de Telegram
TELEGRAM_TOKEN = "7316014813:AAFJCF40Dl_Dsp6lLFZgxKdWyomyuBWZKqg"  # Reemplaza con tu token
TELEGRAM_CHAT_ID = "-4754450530"  # Reemplaza con tu chat_id

# Carpeta para guardar las imágenes
IMAGENES_DIR = "imagenes_ofertas"
os.makedirs(IMAGENES_DIR, exist_ok=True)  # Crear la carpeta si no existe

# Configuración de límites
MENSAJES_POR_LOTE = 10  # Número de ofertas por mensaje 
TIEMPO_ESPERA = 10  # Tiempo de espera entre mensajes 
MAX_REINTENTOS = 3  # Número máximo de reintentos en caso de error

def acortar_url(url):
    """
    Acorta una URL usando el servicio TinyURL.
    """
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        if response.status_code == 200:
            return response.text  # Devuelve la URL acortada
        else:
            return url  # Si hay un error, devuelve la URL original
    except Exception as e:
        print(f"Error al acortar la URL: {e}")
        return url  # Si hay un error, devuelve la URL original

def limpiar_descuento(descuento):
    """
    Limpia el campo descuento y extrae el valor numérico.
    """
    try:
        # Eliminar cualquier texto no numérico (como "OFF")
        descuento_limpio = ''.join(filter(str.isdigit, descuento))
        # Convertir a float
        return float(descuento_limpio)
    except ValueError:
        # Si no se puede convertir, devolver 0
        return 0.0

def descargar_imagen(url_imagen, nombre_archivo):
    """
    Descarga una imagen desde una URL y la guarda localmente.
    """
    try:
        response = requests.get(url_imagen, stream=True)
        if response.status_code == 200:
            with open(nombre_archivo, "wb") as archivo:
                for chunk in response.iter_content(1024):
                    archivo.write(chunk)
            return nombre_archivo
        else:
            print(f"Error al descargar la imagen: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

async def enviar_mensaje_telegram(mensaje, imagen_path=None):
    """
    Envía un mensaje a Telegram, con o sin imagen.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto" if imagen_path else f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    print(f"Enviando mensaje a Telegram: {url}")

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": mensaje if imagen_path else None,  # Usar caption si hay imagen
        "parse_mode": "HTML"  # Usa HTML para formatear el mensaje
    }

    reintentos = 0
    while reintentos < MAX_REINTENTOS:
        try:
            if imagen_path:
                # Enviar imagen
                with open(imagen_path, "rb") as imagen:
                    files = {"photo": imagen}
                    response = requests.post(url, data=payload, files=files, timeout=10)
            else:
                # Enviar solo texto
                payload["text"] = mensaje
                response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                return  # Mensaje enviado correctamente
            else:
                print(f"Error al enviar mensaje a Telegram: {response.text}")
                reintentos += 1
                await asyncio.sleep(TIEMPO_ESPERA * 2)  # Esperar más tiempo en cada reintento
        except Exception as e:
            print(f"Error al enviar mensaje a Telegram: {e}")
            reintentos += 1
            await asyncio.sleep(TIEMPO_ESPERA * 2)  # Esperar más tiempo en cada reintento

    print(f"No se pudo enviar el mensaje después de {MAX_REINTENTOS} reintentos.")

async def main():
    # URL de la página de ofertas
    url = "https://www.mercadolibre.com.mx/ofertas"

    # Extraer todas las ofertas
    print("Iniciando extracción de ofertas...")
    todas_las_ofertas = await extraer_todas_las_ofertas(url)

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

    # Obtener el resultado final (el valor encapsulado en la monada)
    ofertas_finales = monada_ofertas.value

    # Mostrar resultados y enviar a Telegram
    if ofertas_finales and isinstance(ofertas_finales, list):  # Verificar que sea una lista
        print(f"\nTotal de ofertas extraídas: {len(ofertas_finales)}")
        
        # Enviar ofertas en lotes de 4
        for i in range(0, len(ofertas_finales), MENSAJES_POR_LOTE):
            lote = ofertas_finales[i:i + MENSAJES_POR_LOTE]
            mensaje = ""

            for oferta in lote:
                mensaje += (
                    f"<b>Título:</b> {oferta['titulo']}\n"
                    f"<b>Precio actual:</b> {oferta['precio_actual']}\n"
                    f"<b>Precio anterior:</b> ${oferta['precio_anterior']}\n"
                    f"<b>Descuento:</b> {oferta['descuento']}%\n"
                    f"<b>Envío:</b> {oferta['envio']}\n"
                    f"<b>URL:</b> {oferta['url']}\n\n"
                )

            await enviar_mensaje_telegram(mensaje)
            await asyncio.sleep(TIEMPO_ESPERA)  # Esperar entre lotes
    else:
        print("\nNo se encontraron ofertas que cumplan los criterios.")

if __name__ == "__main__":
    asyncio.run(main())  # Ejecutar la función principal de manera asíncrona