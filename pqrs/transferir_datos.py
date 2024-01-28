import json

def transferir_datos():
    try:
        # Abrir el archivo de datos_temp.json para lectura
        with open('datos_temp.json', 'r', encoding='latin-1') as file:
            data = json.load(file)

        # Procesar los datos si es necesario
        # Por ejemplo, aquí podrías realizar transformaciones o filtrar datos
        
        # Escribir los datos procesados en temp_fixture.json
        with open('temp_fixture.json', 'w', encoding='utf-8') as temp_file:
            json.dump(data, temp_file)

        print("Transferencia de datos exitosa.")
    except Exception as e:
        print(f"Error durante la transferencia de datos: {e}")

if __name__ == "__main__":
    transferir_datos()