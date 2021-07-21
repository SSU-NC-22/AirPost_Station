import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library


class LED():
	def __init__(self, gpio=32):
		self.gpio = gpio

		GPIO.setwarnings(False)  # Ignore warning for now
		GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
		GPIO.setup(self.gpio, GPIO.OUT,
		           initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)

	def On(self):
		GPIO.output(self.gpio, GPIO.HIGH)  # Turn on

	def Off(self):
		GPIO.output(self.gpio, GPIO.LOW)  # Turn off
