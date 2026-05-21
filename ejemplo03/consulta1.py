from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la(s) clase(s) del archivo clases
from clases import *

# se importa información del archivo config
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Listar entregas; por cada entrega: nombre estudiante, título de la tarea, nombre del profesor
entregas = session.query(Entrega).all()

for e in entregas:
    print(
        e.estudiante.nombre,
        "|",
        e.tarea.titulo,
        "|",
        e.tarea.curso.instructor.nombre,
    )
