from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuracion import cadena_base_datos
from genera_tablas import Club, Jugador

engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# Importar Clubs
with open("data/datos_clubs.csv", "r", encoding="utf-8") as archivo_clubs:
    lineas_clubs = archivo_clubs.readlines()

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
    
    diccionario_clubs[nombre] = club

session.commit()

# Importar Jugadores
with open("data/datos_jugadores.csv", "r", encoding="utf-8") as archivo_jugadores:
    lineas_jugadores = archivo_jugadores.readlines()

for linea in lineas_jugadores:
    linea = linea.strip()
    if not linea:
        continue
    
    partes = linea.split(";")
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