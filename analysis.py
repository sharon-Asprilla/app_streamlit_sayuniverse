import pandas as pd
import requests

usuarios = requests.get("http://127.0.0.1:8000/usuarios").json()
df_usuarios = pd.DataFrame(usuarios, columns=["id","correo","nombre","fecha_registro"])
print(df_usuarios)

cursos = requests.get("http://127.0.0.1:8000/cursos").json()
df_cursos = pd.DataFrame(cursos, columns=["id","nombre","nivel","descripcion","clases","fecha_inicio"])
print(df_cursos.groupby("nivel")["id"].count())
