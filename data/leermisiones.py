import json
import os


def leer_misiones():
    # Obtiene la ruta al directorio del archivo actual.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    filename = os.path.join(current_dir, "..", "recursos", "misiones", "misiones.json")
    if filename!=None:
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data["misiones"]



def leer_personajes():
    # Obtiene la ruta al directorio del archivo actual.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    filename = os.path.join(current_dir, "..", "recursos", "personajes", "personajes.json")
    if filename!=None:
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data["personajes"]