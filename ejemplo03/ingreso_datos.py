import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from config import cadena_base_datos
from clases import Departamento, Instructor, Curso, Estudiante, Inscripcion, Tarea, Entrega

def parsear_fecha(fecha_str):
    return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")

engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# 1. Importar Departamento
with open("01_departamento.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        departamento = Departamento(
            id=int(linea["id"]),
            nombre=linea["nombre"]
        )
        session.add(departamento)

# 2. Importar Instructor
with open("02_instructor.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        instructor = Instructor(
            id=int(linea["id"]),
            nombre=linea["nombre"]
        )
        session.add(instructor)

session.commit()

# 3. Importar Curso
with open("03_curso.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        departamento_obj = session.query(Departamento).filter_by(id=int(linea["departamento_id"])).one()
        instructor_obj = session.query(Instructor).filter_by(id=int(linea["instructor_id"])).one()
        
        curso = Curso(
            id=int(linea["id"]),
            titulo=linea["titulo"],
            departamento=departamento_obj,
            instructor=instructor_obj
        )
        session.add(curso)

# 4. Importar Estudiante
with open("04_estudiante.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        estudiante = Estudiante(
            id=int(linea["id"]),
            nombre=linea["nombre"]
        )
        session.add(estudiante)

session.commit()

# 5. Importar Inscripcion
with open("05_inscripcion.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        fecha = parsear_fecha(linea["fecha_inscripcion"])
        
        estudiante_obj = session.query(Estudiante).filter_by(id=int(linea["estudiante_id"])).one()
        curso_obj = session.query(Curso).filter_by(id=int(linea["curso_id"])).one()
        
        inscripcion = Inscripcion(
            estudiante=estudiante_obj,
            curso=curso_obj,
            fecha_inscripcion=fecha
        )
        session.add(inscripcion)

# 6. Importar Tarea
with open("06_tarea.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        fecha = parsear_fecha(linea["fecha_entrega"])
        
        curso_obj = session.query(Curso).filter_by(id=int(linea["curso_id"])).one()
        
        tarea = Tarea(
            id=int(linea["id"]),
            curso=curso_obj,
            titulo=linea["titulo"],
            fecha_entrega=fecha
        )
        session.add(tarea)

session.commit()

# 7. Importar Entrega
with open("07_entrega.csv", "r", encoding="utf-8") as archivo:
    reader = csv.DictReader(archivo)
    for linea in reader:
        fecha = parsear_fecha(linea["fecha_envio"])
        
        tarea_obj = session.query(Tarea).filter_by(id=int(linea["tarea_id"])).one()
        estudiante_obj = session.query(Estudiante).filter_by(id=int(linea["estudiante_id"])).one()
        
        entrega = Entrega(
            id=int(linea["id"]),
            tarea=tarea_obj,
            estudiante=estudiante_obj,
            fecha_envio=fecha,
            calificacion=float(linea["calificacion"])
        )
        session.add(entrega)

session.commit()
print("Datos importados exitosamente a la base de datos.")
