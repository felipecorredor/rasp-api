import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading
import websocket
import json
import signal
import sys

semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)
reader = SimpleMFRC522()
is_reading = True

GPIO.setwarnings(False)

TARJETA = 150564635253
LLAVERO = 214018868130

websocket_url = "wss://qti41egldh.execute-api.us-east-1.amazonaws.com/production"

def relay_on(channel):
    semaforo1.state = channel
    semaforo2.state = channel

    semaforo1.paint()

    # websocket
    ws = websocket.create_connection(websocket_url)
    message = {"action": "sendmessage", "message": "websocket connection"}
    ws.send(json.dumps(message))
    ws.close()

def relay_off(channel):
    semaforo1.state = channel
    semaforo2.state = channel

# Capture SIGINT for cleanup
def end_read(signal, frame):
    global is_reading
    print('Ctrl+C captured, exiting')
    is_reading = False
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

while is_reading:
    try:
        id, text = reader.read()
        if id == TARJETA:
            relay_on(2)  
            print(text + ": Access granted")
        elif id == LLAVERO:
            relay_on(1) 
            print(text + ": Access granted")
        else:
            print("Not allowed")
    finally:
        GPIO.cleanup()