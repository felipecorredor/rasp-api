from flask import request
from flask_api import FlaskAPI
from flask_cors import CORS
import threading
from semaforo import Semaforo
from semaforo_esquina import Semaforo_esquina

#freq1=1
semaforo1 = Semaforo(12,16,18,2,0)
semaforo2 = Semaforo(11,13,15,2,0)
semaforo3 = Semaforo_esquina(12,16,18,11,13,15,2,0)

app = FlaskAPI(__name__)
CORS(app)

thsem1=threading.Thread(target=semaforo1.paint)
thsem1.start()
thsem2=threading.Thread(target=semaforo2.paint)
thsem2.start()
thsem3=threading.Thread(target=semaforo3.paint)
thsem3.start()


@app.route('/set_state', methods=["GET", "POST"])
def set_state():
    if request.method == "POST":
        new_state = request.data.get("state")
        if new_state is not None and new_state in [0,1,2,3]:
            semaforo1.state = new_state
            semaforo2.state = new_state
            semaforo3.state = new_state
            return {"message": f"Estado cambiado a {new_state}", "state1": semaforo1.state, "state2": semaforo2.state, "state3": semaforo3.state}
        else:
            return {"error": "Estado no válido"}
    
@app.route('/set_freq', methods=["GET","POST"])
def set_freq():
    if request.method == "POST":
        new_freq = int(request.data.get("freq"))
        semaforo = int(request.data.get("semaforo"))
        if new_freq is not None and semaforo in [1,2,3]:
            #global freq1
            freq1 = new_freq
            if semaforo == 1:
                semaforo1.freq = new_freq
            elif semaforo == 2:
                semaforo2.freq = new_freq
            #elif semaforo == 3:
                #semaforo3.freq = new_freq
            return {"message": f"Frecuencia cambiada a {new_freq}", "freq1": freq1, "semaforo": semaforo}
        else:
            return{"error": "Frecuencia o semáforo no válido"}
if __name__ == "__main__":
    app.run()
