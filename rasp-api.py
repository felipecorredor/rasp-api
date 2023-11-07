from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import threading
from semaforo import Semaforo
from semaforo_esquina import Semaforo_esquina
import time

#freq1=1
semaforo1 = Semaforo(37,35,33,2,0)
semaforo2 = Semaforo(3,5,7,2,0)
semaforo3 = Semaforo_esquina(37,35,33,3,5,7,2,0)

app = FlaskAPI(__name__)
CORS(app)

# Configura la clave secreta para JWT
app.config['JWT_SECRET_KEY'] = '3zsjMDUSBk2M9@'
jwt = JWTManager(app)

thsem1 = threading.Thread(target=semaforo1.paint)
thsem1.start()

thsem2 = threading.Thread(target=semaforo2.paint)
thsem2.start()

thsem3 = threading.Thread(target=semaforo3.paint)
thsem3.start()


# Ejemplo de autenticación con usuario y contraseña
@app.route('/login', methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    
    if username == "user" and password == "password":
        # Genera un token JWT válido
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# Ejemplo de una ruta protegida con autenticación JWT
@app.route('/set_state', methods=["POST"])
@jwt_required()
def set_state():
    if request.method == "POST":
        new_state = request.data.get("state")
        if new_state is not None and new_state in [0,1,2,3]:
            semaforo1.state = new_state
            semaforo2.state = new_state
            semaforo3.state = new_state
            return {"message": f"Estado cambiado a {new_state}", "state1": semaforo1.state, "state2": semaforo2.state, "state3": semaforo3.state }
        else:
            return {"error": "Estado no válido"}

@app.route('/set_freq', methods=["GET","POST"])
@jwt_required()
def set_freq():
    if request.method == "POST":
        new_freq = int(request.data.get("freq"))
        semaforo = int(request.data.get("semaforo"))
        if new_freq is not None and semaforo in [1,2,3]:
            global freq1  # Asigna freq1 como global
            freq1 = new_freq
            if semaforo == 1:
                semaforo1.freq = new_freq
            elif semaforo == 2:
                semaforo2.freq = new_freq
            elif semaforo == 3:
                semaforo3.freq = new_freq
            return {"message": f"Frecuencia cambiada a {new_freq}", "freq1": freq1, "semaforo": semaforo}
        else:
            return {"error": "Frecuencia o semáforo no válido"}

if __name__ == "__main__":

    app.run()
