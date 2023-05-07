import sqlite3

def create_db():

    # Conectar con la base de datos (creará el archivo si no existe)
    conn = sqlite3.connect('juego.db')

    # Crear una tabla para los datos de los jugadores
    conn.execute('''CREATE TABLE IF NOT EXISTS jugadores
    (nombre TEXT, nombre_nave TEXT, karma NUMERIC, poder Numeric)''')
    #karma va a ser del 1 al 10, siendo 5 neutral.
    #poder va a ser de 10 a 100 el poder maximo

    conn.execute('''CREATE TABLE IF NOT EXISTS jugador_eventos 
    (nombrejugador TEXT, numeroevento numeric, visitado boolean, hostil boolean)''')

    # marcaremos si el ha sido evento visitado, y si nuestra accion ha dejado ese evento como hostil o no hostil.
    # Insertar datos de jugador en la tabla

    #conn.execute("INSERT INTO jugadores (nombre, nombre_nave) VALUES (?, ?)", ("Jugador1", "Nivel1"))

    # Guardar cambios en la base de datos
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()