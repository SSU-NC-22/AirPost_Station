"""Simulated adafruit_dht (DHT11 temp/humidity) for SITL — synthetic but plausible readings."""
import math, time
class DHT11:
    def __init__(self, pin, use_pulseio=False): self._pin = pin
    @property
    def temperature(self): return round(20 + 6 * math.sin(time.time() / 17.0), 1)
    @property
    def humidity(self): return round(55 + 15 * math.cos(time.time() / 23.0), 1)
