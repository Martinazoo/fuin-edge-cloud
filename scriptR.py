import serial
import requests
import time
import re

SERIAL_PORT = ''
BAUD_RATE = 9600

API_URL = ''  

PATRON = re.compile(r'Humidity:\s*([\d.]+),Temperature:\s*([\d.]+)')

def leer_datos_arduino():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as arduino:
            time.sleep(2) 
            while True:
                linea = arduino.readline().decode('utf-8').strip()
                if linea:
                    print("Datos recibidos:", linea)
                    datos = parsear_datos(linea)
                    if datos:
                        enviar_a_api(datos)
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serie: {e}")

def parsear_datos(linea):
    match = PATRON.search(linea)
    if match:
        humedad = float(match.group(1))
        temperatura = float(match.group(2))
        return {'temperatura': temperatura, 'humedad': humedad}
    else:
        print("Formato no reconocido:", linea)
        return None

def enviar_a_api(datos):
    try:
        response = requests.post(API_URL, json=datos)
        if response.status_code == 200:
            print("Datos enviados correctamente:", datos)
        else:
            print(f"Error al enviar datos ({response.status_code}): {response.text}")
    except requests.RequestException as e:
        print(f"Error de conexión con la API: {e}")


leer_datos_arduino()
