#!/usr/bin/python

import spidev


class IRSensor():
	def __init__(self, channel=0):
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		self.spi.max_speed_hz = 500000

		self.channel = channel
		self.data = 0

	def ReadChannel(self):
		val = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
		self.data = ((val[1] & 3) << 8) + val[2]

	def read(self):
		v = (self.ReadChannel() / 1023.0) * 3.3
		dist = 16.2537 * v ** 4 - 129.893 * v ** 3 + 382.268 * v ** 2 - 512.611 * v + 301.439
		
		return "Distanz: %.2f cm" % dist
