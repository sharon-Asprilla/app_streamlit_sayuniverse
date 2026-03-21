from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Función para consultar la base de datos
def query_db(query, params=()):
    conn = sqlite3.connect("academia.db")
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

@app.get("/usuarios")
def get_usuarios():
    return query_db("SELECT id, correo, nombre, fecha_registro FROM usuarios")

@app.get("/cursos")
def get_cursos():
    return query_db("SELECT id, nombre, nivel, descripcion, clases, fecha_inicio FROM cursos")

@app.get("/inscripciones/{usuario_id}")
def get_inscripciones(usuario_id: int):
    return query_db("SELECT curso_id, fecha_inscripcion FROM inscripciones WHERE usuario_id=?", (usuario_id,))

@app.get("/certificados/{usuario_id}")
def get_certificados(usuario_id: int):
    return query_db("SELECT curso_id, fecha_emision FROM certificados WHERE usuario_id=?", (usuario_id,))


#exposision de endpoints en la api

import sqlite3
from fastapi import FastAPI

app = FastAPI()

def query_db(query, params=()):
    conn = sqlite3.connect("academia.db")
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

@app.get("/usuarios")
def get_usuarios():
    return query_db("SELECT id, correo, nombre, fecha_registro FROM usuarios")

@app.get("/cursos")
def get_cursos():
    return query_db("SELECT id, nombre, nivel, descripcion, clases, fecha_inicio FROM cursos")
