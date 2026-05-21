from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se importan las clases de genera_tablas
from genera_tablas import Club, Jugador

# se genera el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# Importar Clubs
with open("data/datos_clubs.csv", "r", encoding="utf-8") as archivo_clubs:
    lineas_clubs = archivo_clubs.readlines()

# Diccionario para mapear nombre del club con su objeto de SQLAlchemy
diccionario_clubs = {}

for linea in lineas_clubs:
    linea = linea.strip()
    if not linea:
        continue
    
    partes = linea.split(";")
    nombre = partes[0]
    deporte = partes[1]
    fundacion = int(partes[2])
    
    club = Club(nombre=nombre, deporte=deporte, fundacion=fundacion)
    session.add(club)
    
    # Guardamos en el diccionario para usarlo luego con los jugadores
    diccionario_clubs[nombre] = club

# Guardar los clubs en la base de datos para que se les asigne un ID
session.commit()

# Importar Jugadores
with open("data/datos_jugadores.csv", "r", encoding="utf-8") as archivo_jugadores:
    lineas_jugadores = archivo_jugadores.readlines()

for linea in lineas_jugadores:
    linea = linea.strip()
    if not linea:
        continue
    
    partes = linea.split(";")
    # Formato: Nombre del Club; Posición; Dorsal; Nombre del Jugador
    nombre_club = partes[0]
    posicion = partes[1]
    dorsal = int(partes[2])
    nombre_jugador = partes[3]
    
    club_relacionado = diccionario_clubs.get(nombre_club)
    
    if club_relacionado:
        jugador = Jugador(
            nombre=nombre_jugador,
            dorsal=dorsal,
            posicion=posicion,
            club=club_relacionado
        )
        session.add(jugador)

session.commit()
print("Datos importados exitosamente a la base de datos.")