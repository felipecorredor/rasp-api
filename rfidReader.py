from mfrc522 import MFRC522
import time
from semaforo import Semaforo

lector = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

semaforo1 = Semaforo(37,35,33,2,0)
semaforo2 = Semaforo(3,5,7,2,0)

TARJETA = 150564635253
LLAVERO = 75147236

while True:
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid),"little",False)
            
            if identificador == TARJETA:
                print("UID: "+ str(identificador)+" Acceso concedido")
                semaforo1.state = 2
                semaforo2.state = 2
                
            elif identificador == LLAVERO:
               print("UID: "+ str(identificador)+" Acceso concedido")
               semaforo1.state = 1
               semaforo2.state = 1
                
            else:
                print("UID: "+ str(identificador)+" desconocido: Acceso denegado")