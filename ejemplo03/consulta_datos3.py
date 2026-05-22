# consulta3.py: Listar las inscripciones del departamento de Ciencias de la Computación.
# Por cada inscripción, presentar el 
# nombre del estudiante, el nombre del curso y el nombre del profesor
from clases import Instructor
from clases import Tarea
from clases import Entrega
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Inscripcion, Curso, Departamento
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

inscripciones = session.query(Inscripcion).join(Curso).join(Departamento).filter(
    Departamento.nombre.like("%Compu%")
).all()

print("Inscripciones de Ciencias de la Computación:")
print("--------------------------------------------")

for s in inscripciones:
    print(f"Estudiante: {s.estudiante.nombre}- Curso: {s.curso.titulo}- Profesor: {s.curso.instructor.nombre}")
# practica
# Escribe una consulta que obtenga todas las Entregas (de la clase Entrega) 
# correspondientes a tareas de cursos que sean dictados por la instructora llamada 
# "Lucía Andrade".

# Una vez obtenidas, recorre los resultados con un bucle for e imprime por cada 
# entrega lo siguiente:

# El título de la tarea entregada.
# El nombre del estudiante que la entregó.
# La calificación que sacó.
entregas = session.query(Entrega).join(Tarea).join(Curso).filter(
    Instructor.nombre.like("%Andrade%")
).all()

print("Entregas de Lucía Andrade:")
print("--------------------------------------------")

for e in entregas:
    print(f"Estudiante: {e.estudiante.nombre}- Tarea: {e.tarea.titulo}- Profesor: {e.tarea.curso.instructor.nombre} ")
