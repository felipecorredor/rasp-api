import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from semaforo import Semaforo
import threading
import queue

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

# Cola para coordinar las actualizaciones de semáforos
semaforo_queue = queue.Queue()

# Función para ejecutar semaforo1.paint()
def semaforo1_thread():
    while True:
        semaforo1.paint()
        semaforo_queue.put("Semaforo1")

# Función para ejecutar semaforo2.paint()
def semaforo2_thread():
    while True:
        semaforo2.paint()
        semaforo_queue.put("Semaforo2")

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
    
    # Procesa las actualizaciones de semáforos de la cola
    try:
        while True:
            updated_semaforo = semaforo_queue.get_nowait()
            print(f"Actualizado: {updated_semaforo}")
    except queue.Empty:
        pass
