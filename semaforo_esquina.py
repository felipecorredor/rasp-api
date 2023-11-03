import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

class Semaforo_esquina:
    def __init__(self,rojo1:int,amarillo1:int,verde1:int,rojo2:int,amarillo2:int,verde2:int,freq:float,state:int):
        self.leds = {"rojo1":rojo1,"amarillo1":amarillo1,"verde1":verde1,"rojo2":rojo2,"amarillo2":amarillo2,"verde2":verde2,"freq":freq,"state":state}
        self.freq = freq
        self.state = state
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.leds["rojo1"], GPIO.OUT)
        GPIO.setup(self.leds["amarillo1"], GPIO.OUT)
        GPIO.setup(self.leds["verde1"], GPIO.OUT)
        GPIO.setup(self.leds["rojo2"], GPIO.OUT)
        GPIO.setup(self.leds["amarillo2"], GPIO.OUT)
        GPIO.setup(self.leds["verde2"], GPIO.OUT)
        
    def paint(self):
        while True:
            if self.state == 3:
                GPIO.output(self.leds["rojo1"], True)
                GPIO.output(self.leds["rojo2"], False)
                GPIO.output(self.leds["amarillo1"], False)
                GPIO.output(self.leds["amarillo2"], True)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq)
                GPIO.output(self.leds["rojo1"], True)
                GPIO.output(self.leds["rojo2"], False)
                GPIO.output(self.leds["amarillo1"], False)
                GPIO.output(self.leds["amarillo2"], False)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], True)
                time.sleep(self.freq+0.3)
                GPIO.output(self.leds["rojo1"], True)
                GPIO.output(self.leds["rojo2"], False)
                GPIO.output(self.leds["amarillo1"], False)
                GPIO.output(self.leds["amarillo2"], True)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq)
                GPIO.output(self.leds["rojo1"], True)
                GPIO.output(self.leds["rojo2"], True)
                GPIO.output(self.leds["amarillo1"], False)
                GPIO.output(self.leds["amarillo2"], False)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq-0.6)
                GPIO.output(self.leds["rojo1"], False)
                GPIO.output(self.leds["rojo2"], True)
                GPIO.output(self.leds["amarillo1"], True)
                GPIO.output(self.leds["amarillo2"], False)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq)
                GPIO.output(self.leds["rojo1"], False)
                GPIO.output(self.leds["rojo2"], True)
                GPIO.output(self.leds["amarillo1"], False)
                GPIO.output(self.leds["amarillo2"], False)
                GPIO.output(self.leds["verde1"], True)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq+0.3)
                GPIO.output(self.leds["rojo1"], False)
                GPIO.output(self.leds["rojo2"], True)
                GPIO.output(self.leds["amarillo1"], True)
                GPIO.output(self.leds["amarillo2"], False)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq)
                GPIO.output(self.leds["rojo1"], True)
                GPIO.output(self.leds["rojo2"], True)
                GPIO.output(self.leds["amarillo1"], False)
                GPIO.output(self.leds["amarillo2"], False)
                GPIO.output(self.leds["verde1"], False)
                GPIO.output(self.leds["verde2"], False)
                time.sleep(self.freq-0.6)
                
