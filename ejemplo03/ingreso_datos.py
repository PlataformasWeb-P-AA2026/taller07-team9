from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from config import cadena_base_datos
from clases import Departamento, Instructor, Curso, Estudiante, Inscripcion, Tarea, Entrega

engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

def parsear_fecha(fecha_str):
    return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")

# 1. Importar Departamento
with open("01_departamento.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:] 
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        departamento = Departamento(
            id=int(partes[0]),
            nombre=partes[1]
        )
        session.add(departamento)

# 2. Importar Instructor
with open("02_instructor.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:]
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        instructor = Instructor(
            id=int(partes[0]),
            nombre=partes[1]
        )
        session.add(instructor)

# 3. Importar Curso
with open("03_curso.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:]
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        curso = Curso(
            id=int(partes[0]),
            titulo=partes[1],
            departamento_id=int(partes[2]),
            instructor_id=int(partes[3])
        )
        session.add(curso)

# 4. Importar Estudiante
with open("04_estudiante.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:]
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        estudiante = Estudiante(
            id=int(partes[0]),
            nombre=partes[1]
        )
        session.add(estudiante)

# 5. Importar Inscripcion
with open("05_inscripcion.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:]
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        fecha = parsear_fecha(partes[2])
        inscripcion = Inscripcion(
            estudiante_id=int(partes[0]),
            curso_id=int(partes[1]),
            fecha_inscripcion=fecha
        )
        session.add(inscripcion)

# 6. Importar Tarea
with open("06_tarea.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:]
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        fecha = parsear_fecha(partes[3])
        tarea = Tarea(
            id=int(partes[0]),
            curso_id=int(partes[1]),
            titulo=partes[2],
            fecha_entrega=fecha
        )
        session.add(tarea)

# 7. Importar Entrega
with open("07_entrega.csv", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()[1:]
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        fecha = parsear_fecha(partes[3])
        entrega = Entrega(
            id=int(partes[0]),
            tarea_id=int(partes[1]),
            estudiante_id=int(partes[2]),
            fecha_envio=fecha,
            calificacion=float(partes[4])
        )
        session.add(entrega)

# Confirmar transacciones
session.commit()
print("Datos importados exitosamente a la base de datos.")
