from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuracion import cadena_base_datos
from genera_tablas import Club, Jugador


def cargar_clubs(session, path_archivo):
    """Lee clubs desde un .csv con formato: nombre;deporte;fundacion"""
    with open(path_archivo, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            partes = [p.strip() for p in linea.split(";")]
            if len(partes) != 3:
                continue

            nombre, deporte, fundacion = partes
            try:
                fundacion = int(fundacion)
            except ValueError:
                continue

            if not session.query(Club).filter_by(nombre=nombre).first():
                session.add(Club(nombre=nombre, deporte=deporte, fundacion=fundacion))


def cargar_jugadores(session, path_archivo):
    """Lee jugadores desde un .csv con formato: club;posicion;dorsal;nombre.

    Si una línea viene incompleta (ej. sin dorsal), se ignora.
    """
    with open(path_archivo, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            partes = [p.strip() for p in linea.split(";")]
            if len(partes) != 4:
                continue

            nombre_club, posicion, dorsal, nombre = partes
            try:
                dorsal = int(dorsal)
            except ValueError:
                continue

            club = session.query(Club).filter_by(nombre=nombre_club).first()
            if not club:
                continue

            session.add(Jugador(nombre=nombre, dorsal=dorsal, posicion=posicion, club=club))


def main():
    engine = create_engine(cadena_base_datos)
    Session = sessionmaker(bind=engine)
    session = Session()

    cargar_clubs(session, "data/datos_clubs.csv")
    session.commit()

    cargar_jugadores(session, "data/datos_jugadores.csv")
    session.commit()

    session.close()


if __name__ == "__main__":
    main()
