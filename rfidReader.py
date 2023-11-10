import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading
import websocket
import json
import signal
import sys
import time

semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)
reader = SimpleMFRC522()
is_reading = True

GPIO.setwarnings(False)

TARJETA = 150564635253
LLAVERO = 214018868130

websocket_url = "wss://qti41egldh.execute-api.us-east-1.amazonaws.com/production"

def paint_semaforo():
    while is_reading:
        semaforo1.paint()
        time.sleep(0.1)

paint_thread = threading.Thread(target=paint_semaforo)
paint_thread.daemon = True  # This makes the thread exit when the main program exits
paint_thread.start()

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

# Capture SIGINT for cleanup
def end_read(signal, frame):
    global is_reading
    print('Ctrl+C captured, exiting')
    is_reading = False
    paint_thread.join()  # Wait for the paint_semaforo thread to finish
    GPIO.cleanup()
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
        # No need for GPIO cleanup here, it's done in the signal handler
        pass
