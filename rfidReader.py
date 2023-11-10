import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal
import sys

reader = SimpleMFRC522()
is_reading = True

GPIO.setwarnings(False)

TARJETA = 150564635253
LLAVERO = 214018868130



# Capture SIGINT for cleanup
def end_read(signal, frame):
    global is_reading
    print('Ctrl+C captured, exiting')
    is_reading = False
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

while is_reading:
    try:
        id, text = reader.read()
        print(f'ID :: {id}')
        print(f'Badge Number :: {text}')
    finally:
        GPIO.cleanup()