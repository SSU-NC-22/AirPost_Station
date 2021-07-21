import adafruit_dht
from board import *
import time

# GPIO18
SENSOR_PIN = D18

dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)

while True:
    time.sleep(1)
    try:
        temperature = dht11.temperature
        humidity = dht11.humidity
    except:
        continue
        
    print(f"Humidity= {humidity:.2f}")
    print(f"Temperature= {temperature:.2f}°C")