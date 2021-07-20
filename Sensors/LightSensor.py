import spidev


class LightSensor():
	def __init__(self, channel=0):
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		self.spi.max_speed_hz = 500000

		self.channel = channel
		self.data = 0
		self.volt = 0

	def ReadChannel(self):
		val = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
		self.data = ((val[1] & 3) << 8) + val[2]

	def ConvertVolt(self):
		self.volt = (self.data * 3.3) / float(1023)
		self.volt = round(self.volt, 2)

	def Read(self):
		self.readChannel()
		self.ConvertVolt()
		return [self.data, self.volt]
