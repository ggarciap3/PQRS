from django.core.management import call_command
import json
import subprocess

# Cargar datos desde el archivo JSON
with open('datos_temp.json', 'rb') as file:
    # Usar el codec latin-1 en lugar de utf-8
    data = file.read().decode('latin-1', errors='replace')

# Crear un archivo temporal de fixture
with open('temp_fixture.json', 'w', encoding='utf-8') as temp_file:
    temp_file.write(data)

# Llamar al comando loaddata con el archivo de fixture temporal
subprocess.run(['python', 'manage.py', 'loaddata', '--database=default', 'temp_fixture.json'])
