# myapp/utils.py
from django.db import connections

def obtener_datos_desde_postgres():
    with connections['postgres'].cursor() as cursor:
        cursor.execute("SELECT * FROM usuario;")
        datos = cursor.fetchall()

    return datos