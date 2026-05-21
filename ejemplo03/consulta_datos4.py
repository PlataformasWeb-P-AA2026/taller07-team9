# Por cada curso, presentar sus tareas asociadas.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Curso
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

cursos = session.query(Curso).all()

print("Tareas asociadas por cada curso:")
print("============================================")

for c in cursos:
    print(f"Curso: {c.titulo}")
    
    for t in c.tareas:
        print(f"  - Tarea: {t.titulo} (Entrega: {t.fecha_entrega})")
        
    print("--------------------------------------------")
