import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

class tarjetrfid:
    def __init__(self,start=0):
        self.value = start
    def l_rfid(self):
        while True:
            id= reader.read_id()
            self.value=id
            time.sleep(5)
            self.value=0
    def initialize_sem(self):
        rfid_thread = threading.Thread(target=self.l_rfid)
        rfid_thread = thread.start()
    
