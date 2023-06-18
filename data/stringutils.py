
def wraptext(texto, fuente, width):
    lineas = []
    palabras = texto.split()
    linea_actual = palabras[0]
    for palabra in palabras[1:]:
        if fuente.size(linea_actual + " " + palabra)[0] <= width:
            linea_actual += " " + palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    lineas.append(linea_actual)
    return lineas