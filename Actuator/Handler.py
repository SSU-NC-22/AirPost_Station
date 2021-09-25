import json
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library


class Handler():
    def __init__(self):
        self.led = LED()

    def run(self, msg):
        msg = json.loads(msg.decode())
        if msg['value'] == 1:
            self.led.On()
        if msg['value'] == 0:
            self.led.Off()

class LED():
    def __init__(self, gpio=32):
        self.gpio = gpio
        # Ignore warning for now
        GPIO.setwarnings(False) 
        # Use physical pin numbering 
        # GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(self.gpio, GPIO.OUT, initial=GPIO.LOW)

    def On(self):
        GPIO.output(self.gpio, GPIO.HIGH)  # Turn on

    def Off(self):
        GPIO.output(self.gpio, GPIO.LOW)  # Turn off
