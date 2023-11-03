import time
from mfrc522 import SimpleMFRC522

class TarjetaRFID:
    def __init__(self):
        self.reader = SimpleMFRC522()
        self.value = 0

    def read_id(self):
        try:
            id, _ = self.reader.read()
            return id
        except Exception as e:
            print(f"Error al leer la tarjeta RFID: {e}")
            return None
