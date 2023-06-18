class GameState:
    def __init__(self):
        self.karma = 0
        self.defensa = 0
        self.ataque = 0
        self.vida = 100
        self.nombre_elegido = None

        # y cualquier otra variable que desees almacenar

    def set_karma(self, karma):
        self.karma = karma

    def set_ataque(self, ataque):
        self.ataque = ataque

    def set_defensa(self, defensa):
        self.defensa = defensa

    def set_nombre(self, nombre):
        self.nombre = nombre

    def aumentar_karma(self, cantidad):
        self.karma += cantidad

    def disminuir_karma(self, cantidad):
        self.karma -= cantidad

    def aumentar_vida(self, cantidad):
        self.vida += cantidad

    def disminuir_vida(self, cantidad):
        self.vida -= cantidad

    def aumentar_defensa(self, cantidad):
        self.defensa = cantidad

    def disminuir_defensa(self, cantidad):
        self.defensa = cantidad

    def aumentar_ataque(self, cantidad):
        self.ataque = cantidad

    def disminuir_ataque(self, cantidad):
        self.ataque = cantidad