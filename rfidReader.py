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

# Función para ejecutar semaforo1.paint() en un hilo separado
def semaforo1_thread():
    while True:
        semaforo1.paint()

# Función para ejecutar semaforo2.paint() en un hilo separado
def semaforo2_thread():
    while True:
        semaforo2.paint()

# Inicia los hilos para las funciones de los semáforos
thread1 = threading.Thread(target=semaforo1_thread)
thread2 = threading.Thread(target=semaforo2_thread)
thread1.start()
thread2.start()

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
