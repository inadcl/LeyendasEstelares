
class Alien:
    def __init__(self, alien_json):
        self.keys = alien_json.keys()
        self.defensa = alien_json["defensa"] if "defensa" in self.keys else None
        self.ataque = alien_json["ataque"] if "ataque" in self.keys else None

        self.karma = alien_json["karma"] if "karma" in self.keys else None
        self.nombre = alien_json["nombre"] if "nombre" in self.keys else None
        self.image = alien_json["image"] if "image" in self.keys else None