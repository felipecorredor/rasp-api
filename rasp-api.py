from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import threading
import time
import asyncio
import websockets
from tarjetrfid import TarjetaRFID  # Asegúrate de que esta importación sea correcta
import json

# Otras importaciones y configuraciones aquí...

app = FlaskAPI(__name__)
CORS(app)

# Otras configuraciones aquí...

id = TarjetaRFID()  # Inicializa la instancia del lector RFID

# Función para enviar lectura RFID al WebSocket
async def enviar_lectura_al_websocket():
    websocket_url = "wss://qti41egldh.execute-api.us-east-1.amazonaws.com/production"
    message = {"action": "sendmessage", "message": "hello, everyone!"}
    message_json = json.dumps(message)

    async with websockets.connect(websocket_url) as websocket:
        while True:
            rfid_value = id.read_id()
            print("enviar_lectura_al_websocket")
            await websocket.send(message_json)

            if rfid_value:
                # Enviar la lectura al WebSocket
                await websocket.send(message)
            await asyncio.sleep(1)

def rfiid_loop(id):
    while True:
        rfid_value = id.read_id()
        if rfid_value == 150564635253:
            if semaforo1.state != 2:
                semaforo1.state = 2
                semaforo2.state = 2
            else:
                semaforo1.state = 0
                semaforo2.state = 0
            print({"success": "Es tarjeta válida"})
            
            # Inicia el envío al WebSocket en un hilo separado
            print("rfiid_loop")
            asyncio.create_task(enviar_lectura_al_websocket())

        elif rfid_value == 214018868130:
            if semaforo1.state != 2:
                semaforo1.state = 2
                semaforo2.state = 2
            else:
                semaforo1.state = 0
                semaforo2.state = 0
            print({"success": "Es llavero válido"})

            # Inicia el envío al WebSocket en un hilo separado
            rfiid_loop("rfiid_loop::else")
            asyncio.create_task(enviar_lectura_al_websocket())

        else:
            print({"error": "Intento inválido de tarjeta o llavero"})
        time.sleep(1)

# Rutas y otras funciones aquí...

# Resto del código...

if __name__ == "__main__":
    # Hilo para la lectura de tarjetas RFID
    thread_rfiid = threading.Thread(target=rfiid_loop, args=(id,))
    thread_rfiid.start()

    print("this is: __main__")
    app.run()
