import json


class Jugador:
    def __init__(self, karma, nombre, poder):
        self.karma = karma
        self.nombre = nombre
        self.poder = poder
        self.vivo = True

    # Getter para obtener el nombre
    def get_vivo(self):
        return self.vivo

    def get_nombre(self):
        return self.nombre

    def get_Karma(self):
        return self.karma

    def set_Karma(self, karma):
        self.karma = karma

    # Getter para obtener la edad
    def get_poder(self):
        return self.poder

    # Setter para establecer la edad
    def set_poder(self, poder):
        self.poder = poder
