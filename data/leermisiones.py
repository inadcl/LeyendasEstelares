import json
import os

filename = os.path.join("recursos", os.path.join("misiones", "misiones.json"))

def leer_misiones():
    with open(filename, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data["misiones"]
