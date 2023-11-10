import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading
import websocket
import json
import time

semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)
rfid = SimpleMFRC522()
TARJETA = 150564635253
LLAVERO = 214018868130

websocket_url = "wss://qti41egldh.execute-api.us-east-1.amazonaws.com/production"

def establish_websocket_connection():
    try:
        ws = websocket.create_connection(websocket_url)
        return ws
    except Exception as e:
        print(f"Error establishing websocket connection: {e}")
        return None

def relay_on(channel, ws):
    semaforo1.state = channel
    semaforo2.state = channel

    if ws:
        message = {"action": "sendmessage", "message": "websocket connection"}
        ws.send(json.dumps(message))

def relay_off(channel):
    semaforo1.state = channel
    semaforo2.state = channel

def read_rfid(ws):
    while True:
        id, text = rfid.read()
        print(id)
        if id == TARJETA:
            relay_on(2, ws)
            print(text + ": Access granted")
        elif id == LLAVERO:
            relay_on(1, ws)
            print(text + ": Access granted")
        else:
            print("Not allowed")

def control_semaforo_uno():
    while True:
        semaforo1.paint()

# def control_semaforo_dos():
#     while True:
#         semaforo2.paint()

# Establecer la conexión fuera de los bucles
ws = establish_websocket_connection()

thread_rfid = threading.Thread(target=read_rfid, args=(ws,))
thread_semaforo_uno = threading.Thread(target=control_semaforo_uno)
# thread_semaforo_dos = threading.Thread(target=control_semaforo_dos)

thread_rfid.start()
thread_semaforo_uno.start()
# thread_semaforo_dos.start()

# Esperar antes de cerrar el programa
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Manejar interrupción de teclado (Ctrl+C)
    GPIO.cleanup()
    if ws:
        ws.close()
