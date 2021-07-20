import adafruit_dht
from board import *


class TempHumidSensor():
	def __init__(self, gpio=D18):
		self.gpio = gpio
		self.dht11 = adafruit_dht.DHT11(gpio, use_pulseio=False)
		self.temperature = 0
		self.humidity = 0

	def ReadTemperature(self):
		try:
			self.temperature = self.dht11.temperature
			return self.temperature

		except:
			return -1

	def ReadHumidity(self):
		try:
			self.humidity = self.dht11.humidity
			return self.humidity

		except:
			return -1
