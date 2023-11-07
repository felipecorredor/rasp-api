import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo

import threading

semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)

# thsem1 = threading.Thread(target=semaforo1.paint)
# thsem1.start()

# thsem2 = threading.Thread(target=semaforo2.paint)
# thsem2.start()

rfid = SimpleMFRC522()

TARJETA = 150564635253
LLAVERO = 75147236

def relay_on(channel):
    semaforo1.state = channel
    semaforo2.state = channel

def relay_off(channel):
    semaforo1.state = channel
    semaforo2.state = channel

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
        print("Not allowed...")
