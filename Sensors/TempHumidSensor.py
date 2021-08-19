import adafruit_dht
from board import *


class TempHumidSensor():
	def __init__(self, gpio=D18):
		self.gpio = gpio
		self.dht11 = adafruit_dht.DHT11(gpio, use_pulseio=False)
		self.temperature = 0
		self.humidity = 0

	def Read(self):
		try:
			self.temperature = self.dht11.temperature
			self.humidity = self.dht11.humidity

			return [self.temperature, self.humidity]
		except:
			self.temperature = None
			self.humidity = None

			return [self.temperature, self.humidity]
