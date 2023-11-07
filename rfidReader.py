import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading

semaforo1 = Semaforo(37, 35, 33, 2, 0)
semaforo2 = Semaforo(3, 5, 7, 2, 0)
rfid = SimpleMFRC522()
TARJETA = 150564635253
LLAVERO = 214018868130

def relay_on(channel):
    semaforo1.state = channel
    semaforo2.state = channel

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

def control_semaforos():
    while True:
        semaforo1.paint()
        semaforo2.paint()

# Crear hilos para cada bucle
thread_rfid = threading.Thread(target=read_rfid)
thread_semaforos = threading.Thread(target=control_semaforos)

# Iniciar los hilos
thread_rfid.start()
thread_semaforos.start()