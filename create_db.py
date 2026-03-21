import sqlite3



import pandas as pd


conn = sqlite3.connect("academia.db")
df_historial = pd.read_sql("SELECT * FROM historial", conn)
print(df_historial.groupby("accion")["id"].count())




# Crear conexión a la base de datos (se genera academia.db en tu carpeta)
conn = sqlite3.connect("academia.db")
c = conn.cursor()

# Crear tablas
c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE,
    password TEXT,
    nombre TEXT,
    fecha_registro TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    nivel TEXT,
    descripcion TEXT,
    clases INTEGER,
    fecha_inicio TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    curso_id INTEGER,
    fecha_inscripcion TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS certificados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    curso_id INTEGER,
    fecha_emision TEXT,
    archivo TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS evaluaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id INTEGER,
    titulo TEXT,
    fecha_limite TEXT,
    estado TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS actividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    curso_id INTEGER,
    archivo TEXT,
    fecha_entrega TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    mensaje TEXT,
    tipo TEXT,
    fecha TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    accion TEXT,
    fecha TEXT
)""")

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente: academia.db")


# Insertar cursos iniciales si no existen
cursos_iniciales = [
    ("Inglés Básico 1", "Básico", "Saludos y vocabulario esencial", 10, "2026-04-05"),
    ("Inglés Básico 2", "Básico", "Frases comunes y diálogos simples", 12, "2026-04-12"),
    ("Inglés Básico 3", "Básico", "Gramática inicial y conversación", 15, "2026-04-20"),
    ("Inglés Intermedio 1", "Intermedio", "Gramática avanzada y tiempos verbales", 14, "2026-04-10"),
    ("Inglés Intermedio 2", "Intermedio", "Comprensión de textos y conversaciones", 16, "2026-04-18"),
    ("Inglés Intermedio 3", "Intermedio", "Escritura básica y práctica oral", 18, "2026-04-25"),
    ("Inglés Avanzado 1", "Avanzado", "Conversaciones complejas y vocabulario académico", 20, "2026-04-15"),
    ("Inglés Avanzado 2", "Avanzado", "Redacción de ensayos y artículos", 22, "2026-04-22"),
    ("Inglés Avanzado 3", "Avanzado", "Inglés profesional y presentaciones", 25, "2026-04-30")
]

for curso in cursos_iniciales:
    try:
        c.execute("INSERT INTO cursos (nombre, nivel, descripcion, clases, fecha_inicio) VALUES (?,?,?,?,?)", curso)
    except:
        pass

conn.commit()
conn.close()

