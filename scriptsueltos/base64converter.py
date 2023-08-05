import argparse
import base64
import datetime
import os

def base64_to_image(data, output_path):
    # Quita el prefijo "data:image/png;base64,".
    base64_string = data.split(",")[1]

    # Decodifica el valor Base64 a bytes.
    decoded_data = base64.b64decode(base64_string)

    # Guarda los datos decodificados en un archivo de imagen.
    with open(output_path, "wb") as f:
        f.write(decoded_data)

    # Devuelve la ruta absoluta del archivo de imagen.
    return os.path.abspath(output_path)

if __name__ == "__main__":
    # Configura un analizador de argumentos.
    parser = argparse.ArgumentParser(description="Decodifica una imagen en base64 y guarda el resultado.")
    parser.add_argument("base64", help="La cadena base64 a decodificar.")

    # Analiza los argumentos de la línea de comandos.
    args = parser.parse_args()

    # Genera un nombre de archivo basado en el timestamp actual.
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = f"{timestamp}.png"

    # Convierte la imagen base64 a un archivo de imagen y obtiene la ruta absoluta.
    image_path = base64_to_image(args.base64, output_path)
    print(image_path)