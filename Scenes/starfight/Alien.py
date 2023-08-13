
class Alien:
    def __init__(self, alien_json):
        self.defensa = alien_json["defensa"]
        self.ataque = alien_json["ataque"]
        self.karma = alien_json["karma"]
        self.nombre = alien_json["nombre"]
        self.image = alien_json["image"]