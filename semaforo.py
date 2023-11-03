import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Semaforo:
        
    def __init__(self, red:int, yellow:int, green:int, freq:int, state:int):
        self.leds = {"red": red, "yellow": yellow, "green": green}
        self.freq = freq
        self.state = state
        GPIO.setup(self.leds["red"], GPIO.OUT)
        GPIO.setup(self.leds["yellow"], GPIO.OUT)
        GPIO.setup(self.leds["green"], GPIO.OUT)

    def paint(self):
        while True:
            if self.state == 0:
                GPIO.output(self.leds["red"], False)
                GPIO.output(self.leds["yellow"], False)
                GPIO.output(self.leds["green"], False)

            if self.state == 1:
                GPIO.output(self.leds["red"], True)
                GPIO.output(self.leds["yellow"], False)
                GPIO.output(self.leds["green"], False)
                time.sleep(self.freq)
                GPIO.output(self.leds["red"], False)
                GPIO.output(self.leds["yellow"], True)
                time.sleep(self.freq)
                GPIO.output(self.leds["yellow"], False)
                GPIO.output(self.leds["green"], True)
                time.sleep(self.freq)
                GPIO.output(self.leds["yellow"], True)
                GPIO.output(self.leds["green"], False)

            if self.state == 2:
                GPIO.output(self.leds["red"], False)
                GPIO.output(self.leds["yellow"], True)
                GPIO.output(self.leds["green"], False)
                time.sleep(self.freq)
                GPIO.output(self.leds["yellow"], False)
                time.sleep(self.freq)

