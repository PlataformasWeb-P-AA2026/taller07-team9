from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la(s) clase(s) del archivo clases
from clases import *

# se importa información del archivo config
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Listar cursos cuyos profesores tengan "Zam" en su nombre
cursos = (
    session.query(Curso)
    .join(Curso.instructor)
    .filter(Instructor.nombre.like("%Zam%"))
    .all()
)

for c in cursos:
    print(c.titulo, "|", c.instructor.nombre)
