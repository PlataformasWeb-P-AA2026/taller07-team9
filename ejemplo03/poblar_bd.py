import csv
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import cadena_base_datos
from clases import Departamento, Instructor, Curso, Estudiante, Inscripcion, Tarea, Entrega


def parse_datetime(valor: str):
    # Formato en los CSV: 2026-04-02 09:00:00
    return datetime.strptime(valor.strip(), "%Y-%m-%d %H:%M:%S")


def cargar_departamentos(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(Departamento(id=int(row["id"]), nombre=row["nombre"].strip()))


def cargar_instructores(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(Instructor(id=int(row["id"]), nombre=row["nombre"].strip()))


def cargar_cursos(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(
                Curso(
                    id=int(row["id"]),
                    titulo=row["titulo"].strip(),
                    departamento_id=int(row["departamento_id"]),
                    instructor_id=int(row["instructor_id"]),
                )
            )


def cargar_estudiantes(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(Estudiante(id=int(row["id"]), nombre=row["nombre"].strip()))


def cargar_inscripciones(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(
                Inscripcion(
                    estudiante_id=int(row["estudiante_id"]),
                    curso_id=int(row["curso_id"]),
                    fecha_inscripcion=parse_datetime(row["fecha_inscripcion"]),
                )
            )


def cargar_tareas(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(
                Tarea(
                    id=int(row["id"]),
                    curso_id=int(row["curso_id"]),
                    titulo=row["titulo"].strip(),
                    fecha_entrega=parse_datetime(row["fecha_entrega"]),
                )
            )


def cargar_entregas(session, archivo):
    with open(archivo, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(
                Entrega(
                    id=int(row["id"]),
                    tarea_id=int(row["tarea_id"]),
                    estudiante_id=int(row["estudiante_id"]),
                    fecha_envio=parse_datetime(row["fecha_envio"]),
                    calificacion=float(row["calificacion"]),
                )
            )


def main():
    engine = create_engine(cadena_base_datos)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Importante: respetar el orden por llaves foráneas
    cargar_departamentos(session, "01_departamento.csv")
    cargar_instructores(session, "02_instructor.csv")
    cargar_cursos(session, "03_curso.csv")
    cargar_estudiantes(session, "04_estudiante.csv")
    cargar_inscripciones(session, "05_inscripcion.csv")
    cargar_tareas(session, "06_tarea.csv")
    cargar_entregas(session, "07_entrega.csv")

    session.commit()
    session.close()


if __name__ == "__main__":
    main()
