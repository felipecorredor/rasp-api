import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading
import websocket
import json

semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)
rfid = SimpleMFRC522()
TARJETA = 150564635253
LLAVERO = 214018868130

websocket_url = "wss://qti41egldh.execute-api.us-east-1.amazonaws.com/production"

def relay_on(channel):
    semaforo1.state = channel
    semaforo2.state = channel

    # websocket
    ws = websocket.create_connection(websocket_url)
    message = {"action": "sendmessage", "message": "websocket connection"}
    ws.send(json.dumps(message))
    ws.close()

def relay_off(channel):
    semaforo1.state = channel
    semaforo2.state = channel

def read_rfid():
    while True:
        id, text = rfid.read()
        print(id)
        if id == TARJETA:
            relay_on(2)  
            print(text + ": Access granted")
        elif id == LLAVERO:
            relay_on(1) 
            print(text + ": Access granted")
        else:
            print("Not allowed")

def control_semaforo_one():
    try:
        while True:
            semaforo1.paint()
    except Exception as e:
        print(f"Error en control_semaforo_one: {str(e)}")        

# def control_semaforo_two():
#     try:
#         while True:
#             semaforo2.paint()
#     except Exception as e:
#         print(f"Error en control_semaforo_two: {str(e)}")

thread_rfid = threading.Thread(target=read_rfid)
thread_rfid.start()

thread_semaforo_one = threading.Thread(target=control_semaforo_one)
thread_semaforo_one.start()


# thread_semaforo_two = threading.Thread(target=control_semaforo_two)
# thread_semaforo_two.start()
