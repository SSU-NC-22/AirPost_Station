import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=500000
 
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data

def ConvertVolt(data, places):
    volt = (data * 3.3)/float(1023)
    volt = round(volt, places)
    return volt

if __name__ == "__main__":
  while(1):
    light_level = readChannel(0)
    light_volt = ConvertVolt(light_level, 2)
    print("Light Data : {} ({}V)".format(light_level, light_volt))
    time.sleep(0.5)
