# SAY UNIVERSE PROYECTO 

# 📘 Academia App

Aplicación académica desarrollada con **Streamlit**, **FastAPI**, **SQLite** y **Pandas**.  
Incluye login, cursos, inscripciones, certificados, evaluaciones, actividades, alertas e historial.  
Además, expone una API para consumir datos y analizarlos con Pandas.

---

## 🚀 Tecnologías y dependencias

### Backend / API
- **FastAPI** → Framework para crear la API REST.  
- **Uvicorn** → Servidor ASGI para correr la API.  
- **SQLite3** → Base de datos ligera y local.  

### Frontend / Dashboard
- **Streamlit** → Framework para construir la interfaz gráfica interactiva.  

### Análisis de datos
- **Pandas** → Librería para análisis y manipulación de datos.  
- **Requests** → Para consumir la API desde el Dashboard y análisis.  
### creacion de entorno  virtual 
pero no se subio 

### explicacion del proyecto y su estructura mas a detaller y la ejecucion

🗄️ Base de datos
La base de datos academia.db se crea con el script create_db.py.
Tablas incluidas:

usuarios → login y registro.

cursos → catálogo de cursos.

inscripciones → relación usuario-curso.

certificados → certificados emitidos.

evaluaciones → evaluaciones por curso.

actividades → entregas de actividades.

alertas → notificaciones para el usuario.

historial → registro de acciones realizadas

## Ejecucion
python create_db.py

## consumo de api con pandas
creacion de appi 

# 🌐 API Académica

La API se creó con **FastAPI** y se ejecuta con **Uvicorn**.  
Su propósito es exponer los datos de la base de datos `academia.db` para que puedan ser consumidos desde el Dashboard en Streamlit o analizados con Pandas.

---

## 🚀 Tecnologías usadas

- **FastAPI** → Framework para construir la API REST.  
- **Uvicorn** → Servidor ASGI para correr la API.  
- **SQLite3** → Base de datos local y ligera.  
- **Pandas** → Para análisis de datos una vez consumidos los endpoints.  
- **Requests** → Para consumir la API desde Python.

- su ejecutable es : uvicorn api:app --reload --port 8000


Instalación:
```bash
pip install fastapi uvicorn pandas requests


## otra sesion 
Agrega robots.txt y sitemap.xml para indexación en Google

### Instalación de dependencias
```bash
pip install fastapi uvicorn streamlit pandas requests.

### estructura del proyecto 


├── create_db.py    # Script para crear la base de datos
├── academia.db     # Base de datos SQLite (se genera automáticamente)
├── README.md       # Documentación del proyecto
└── .gitignore      # Archivos ignorados por Git


Diagrama relacional

    usuarios ||--o{ inscripciones : "se inscribe"
    cursos ||--o{ inscripciones : "tiene"
    usuarios ||--o{ certificados : "recibe"
    cursos ||--o{ certificados : "otorga"
    cursos ||--o{ evaluaciones : "incluye"
    usuarios ||--o{ actividades : "entrega"
    usuarios ||--o{ alertas : "recibe"
    usuarios ||--o{ historial : "genera"



