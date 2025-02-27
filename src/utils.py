def map_ofertas(ofertas, func):
    return [func(oferta) for oferta in ofertas]

def filter_ofertas(ofertas, criterio):
    """
    Filtra las ofertas según un criterio.
    """
    ofertas_filtradas = []
    for oferta in ofertas:
        try:
            # Limpiar el precio actual (eliminar "$" y comas) y convertirlo a float
            if isinstance(oferta['precio_actual'], str):  # Verificar si es una cadena
                precio_actual = oferta['precio_actual'].replace('$', '').replace(',', '')
                oferta['precio_actual'] = float(precio_actual)
            elif isinstance(oferta['precio_actual'], (int, float)):  # Si ya es un número
                oferta['precio_actual'] = float(oferta['precio_actual'])
            else:
                raise ValueError("Formato de precio no válido")

            # Aplicar el criterio de filtrado
            if criterio(oferta):
                ofertas_filtradas.append(oferta)
        except Exception as e:
            print(f"Error al filtrar oferta: {e}")
    return ofertas_filtradas

def reducir_ofertas(ofertas, func, inicial):
    resultado = inicial
    for oferta in ofertas:
        resultado = func(resultado, oferta)
    return resultado