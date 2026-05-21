# consulta3.py: Listar las inscripciones del departamento de Ciencias de la Computación.
# Por cada inscripción, presentar el 
# nombre del estudiante, el nombre del curso y el nombre del profesor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Inscripcion, Curso, Departamento
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Realizamos el JOIN usando directamente las entidades y filtramos por el nombre
inscripciones = session.query(Inscripcion).join(Curso).join(Departamento).filter(
    Departamento.nombre.like("%Compu%")
).all()

print("Inscripciones de Ciencias de la Computación:")
print("--------------------------------------------")

for s in inscripciones:
    print(f"Estudiante: {s.estudiante.nombre}- Curso: {s.curso.titulo}- Profesor: {s.curso.instructor.nombre}")

