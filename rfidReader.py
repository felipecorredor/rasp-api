import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading
import websocket
import json
import signal
import sys

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Initialize traffic lights
semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)

# Initialize RFID reader
reader = SimpleMFRC522()
is_reading = True

# GPIO setup
GPIO.setwarnings(False)

# RFID card IDs
TARJETA = 150564635253
LLAVERO = 214018868130

# Websocket setup
websocket_url = "wss://qti41egldh.execute-api.us-east-1.amazonaws.com/production"

# Function to handle turning on the relays and updating traffic light states
def relay_on(channel):
    # semaforo1.state = channel
    # semaforo2.state = channel

    # Update the traffic lights
    # semaforo1.paint()
    # semaforo2.paint()

    # WebSocket
    ws = websocket.create_connection(websocket_url)
    message = {"action": "sendmessage", "message": "websocket connection"}
    ws.send(json.dumps(message))
    ws.close()

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
            print(text + ": Access granted")
            # relay_on(2)  
        elif id == LLAVERO:
            print(text + ": Access granted")
            relay_on(1) 
        else:
            print("Not allowed")
    finally:
        # Avoid GPIO cleanup inside the loop
        pass
