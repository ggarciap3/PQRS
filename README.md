# PQRS
 Proyecto Nuevo v.1

Exportar datos
1) ejecuto en el terminal python manage.py dumpdata myapp.Usuario --database=postgres --indent=2 --output=datos_temp.json
2) ejeculto en el terminal python transferir_datos.py
3)  ejecuto en el terminal python manage.py loaddata temp_fixture.json