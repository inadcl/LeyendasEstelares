from data.leermisiones import leer_misiones


class GameState:
    def __init__(self):
        self.karma = 0
        self.defensa = 0
        self.ataque = 0
        self.vida = 100
        self.nombre = None
        self.imagen= ""
        self.misiones = leer_misiones()
        self.clock = None
        print(len(self.misiones))
        # y cualquier otra variable que desees almacenar


    def get_delta_time(self):
        dt = self.clock.tick(60) / 1000.0  # tiempo en segundos desde el último frame
        return dt
    def set_karma(self, karma):
        self.karma = karma

    def set_ataque(self, ataque):
        self.ataque = ataque

    def set_defensa(self, defensa):
        self.defensa = defensa

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_imagen(self, imagen):
        self.imagen = imagen

    def aumentar_karma(self, cantidad):
        self.karma = self.karma + cantidad

    def disminuir_karma(self, cantidad):
        self.karma = self.karma - cantidad

    def aumentar_vida(self, cantidad):
        self.vida = self.vida + cantidad

    def disminuir_vida(self, cantidad):
        self.vida = self.vida - cantidad

    def aumentar_defensa(self, cantidad):
        self.defensa = self.defensa + cantidad

    def disminuir_defensa(self, cantidad):
        self.defensa = self.defensa - cantidad

    def aumentar_ataque(self, cantidad):
        self.ataque = self.ataque + cantidad

    def disminuir_ataque(self, cantidad):
        self.ataque = self.ataque - cantidad

    def tratar_karma(self, param):
        if "+" in param:
            param = param.replace("+", "")
            self.aumentar_karma(int(param))
        elif "-" in param:
            param = param.replace("-", "")
            self.disminuir_karma(int(param))


    def tratar_defensa(self, param):
        if "+" in param:
            param = param.replace("+", "")
            self.aumentar_defensa(int(param))
        elif "-" in param:
            param = param.replace("-", "")
            self.disminuir_defensa(int(param))
    def tratar_ataque(self, param):
        if "+" in param:
            param = param.replace("+", "")
            self.aumentar_ataque(int(param))
        elif "-" in param:
            param = param.replace("-", "")
            self.disminuir_ataque(int(param))