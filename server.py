from flask import Flask, request
import os
import re
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/autores")
def crear_autor():

    data = request.get_json()

    if not all(key in data for key in ["nombre", "apellido"]):
        return {"error": "Faltan campos obligatorios"}, 400
    if not isinstance(data["nombre"], str) or not isinstance(data["apellido"], str):
        return {"error": "Nombre y apellido deben ser cadenas de texto"}, 400
    if "fecha_nacimiento" in data:
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", data["fecha_nacimiento"]):
            return {"error": "Formato de fecha inválido"}, 400
        try:
            fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%d-%m-%Y").date()
        except ValueError:
            return {"error": "Fecha de nacimiento inválida"}, 400

    nombre = data["nombre"]
    apellido = data["apellido"]
    try:
        fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%d-%m-%Y").date() #dia-mes-año
    except KeyError:
        fecha_nacimiento = datetime.now(timezone.utc).date()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(TABLA_AUTORES_INIT)
            cursor.execute(AUTOR_INSERTAR, (nombre, apellido, fecha_nacimiento))
            mensaje = {"mensaje": "Autor " + nombre + " " + apellido + " agregado"}
    return mensaje, 201

@app.get("/autores")
def consultar_autores():
    with connection.cursor() as cursor:
        cursor.execute(AUTORES_CONSULTA)
        autores = cursor.fetchall()
    return autores, 200

@app.get("/autores/<id>")
def consultar_autor(id):
    with connection.cursor() as cursor:
        cursor.execute(AUTOR_CONSULTA, (id,))
        autor = cursor.fetchall()
    return autor, 200

@app.put("/autores/<id>")
def editar_autor(id):
    data = request.get_json()
    campos_permitidos = ["nombre", "apellido", "fecha_nacimiento"]
    if not all(k in campos_permitidos for k in data):
        return {"error": "Campos no permitidos"}, 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM autores WHERE id = %s", (id,))
        autor = cursor.fetchone()
        if not autor:
            return {"error": "Autor no encontrado"}, 404
    
    AUTOR_ACTUALIZA = (
        "UPDATE autores SET nombre = %(nombre)s, apellido = %(apellido)s, fecha_nacimiento = %(fecha_nacimiento)s WHERE id = %(id)s;"
        )
    data["id"]=id
    with connection.cursor() as cursor:
        cursor.execute(AUTOR_ACTUALIZA, data)
        connection.commit()
        mensaje = {"mensaje": "Autor actualizado"}
        return mensaje, 201

@app.delete("/autores/<id>")
def borrar_autor(id):
    with connection.cursor() as cursor:
        cursor.execute(AUTOR_LIBROS_CONSULTA, id)
        autor_libros = cursor.fetchall()
        if len(autor_libros)>0:
            mensaje = {"Mensaje": "No puedes borrar autores con libros existentes"}
            return mensaje
        else:
            cursor.execute(AUTOR_BORRAR, id)
            mensaje = {"mensaje": "Autor eliminado"}
            return mensaje

@app.post("/libros")
def crear_libro():
    data = request.get_json()
    if not all(key in data for key in ["titulo", "fecha_publicacion", "autor_id"]):
        return {"error": "Faltan campos obligatorios"}, 400
    try:
        fecha_publicacion = datetime.strptime(data["fecha_publicacion"], "%d-%m-%Y").date()
    except ValueError:
        return {"error": "Formato de fecha inválido"}, 400
    

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM autores WHERE id = %s", (data["autor_id"],))
        autor = cursor.fetchone()
        if not autor:
            return {"error": "Autor no encontrado"}, 404

    titulo = data["titulo"]
    autor_id = data["autor_id"]
    
    with connection.cursor() as cursor:
        cursor.execute(TABLA_LIBROS_INIT)
        cursor.execute(LIBRO_INSERTAR, (titulo, fecha_publicacion, autor_id))
        mensaje = {"mensaje": "Libro " + titulo + " agregado"}
    return mensaje, 201

@app.get("/libros")
def consultar_libros():
    with connection.cursor() as cursor:
        cursor.execute(LIBROS_CONSULTA)
        autores = cursor.fetchall()
    return autores, 200

@app.get('/libros/<id>')
def consultar_libro(id):
    with connection.cursor() as cursor:
        cursor.execute(LIBRO_CONSULTA, (id,))
        libro = cursor.fetchall()

        if libro is None:
            return {"error": "Libro no encontrado"}, 404

    return libro, 200

@app.put("/libros/<id>")
def editar_libro(id):
    data = request.get_json()
    campos_permitidos = ["titulo", "fecha_publicacion", "autor_id"]
    if not all(k in campos_permitidos for k in data):
        return {"error": "Campos no permitidos"}, 400
        
    libro = consultar_libro(id)
    if not libro:
        return {"error": "Libro no encontrado"}, 404

    LIBRO_ACTUALIZA = (
        "UPDATE libros SET titulo = %(titulo)s, fecha_publicacion = %(fecha_publicacion)s, autor_id = %(autor_id)s WHERE id = %(id)s;"
        )
    data["id"]=id
    with connection.cursor() as cursor:
        cursor.execute(LIBRO_ACTUALIZA, data)
        connection.commit()
        mensaje = {"mensaje": "Libro actualizado"}
        return mensaje, 201

@app.delete("/libros/<id>")
def borrar_libro(id):
    libro = consultar_libro(id)
    if not libro:
        return {"error": "Libro no encontrado"}, 404
    
    with connection.cursor() as cursor:
        cursor.execute(LIBRO_BORRAR, id)
        mensaje = {"mensaje":"Libro eliminado correctamente"}
        return mensaje, 202
    return 505

#Queries

TABLA_AUTORES_INIT = (
    "CREATE TABLE IF NOT EXISTS autores (id SERIAL PRIMARY KEY, nombre TEXT, apellido TEXT, fecha_nacimiento DATE);"
)

AUTOR_INSERTAR = (
    "INSERT INTO autores (nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s);"
)

AUTORES_CONSULTA = (
    "SELECT * FROM autores;"
)

AUTOR_CONSULTA = (
    "SELECT * FROM autores WHERE id = %s;"
)

AUTOR_LIBROS_CONSULTA = (
    "SELECT * FROM libros WHERE autor_id = %s"
)

AUTOR_BORRAR = (
    "DELETE FROM autores WHERE id = %s"
)

TABLA_LIBROS_INIT = (
    "CREATE TABLE IF NOT EXISTS libros (id SERIAL PRIMARY KEY, titulo TEXT, fecha_publicacion DATE, autor_id INTEGER, FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE CASCADE);"
)

LIBRO_INSERTAR = (
    "INSERT INTO libros (titulo, fecha_publicacion, autor_id) VALUES (%s, %s, %s);"
)

LIBROS_CONSULTA = (
    "SELECT * FROM libros;"
)

LIBRO_CONSULTA = (
    "SELECT * FROM libros WHERE id = %s;"
)

LIBRO_BORRAR = (
    "DELETE FROM libros WHERE id = %s"
)

if __name__ == "__main__":
    app.run(debug=True, port=8080)