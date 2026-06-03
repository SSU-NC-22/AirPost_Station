"""Simulated spidev (SPI ADC) for the station's light sensor in SITL. The real LightSensor reads a
3-byte SPI frame where data = ((val[1]&3)<<8)+val[2] (a 0-1023 ADC reading). We synthesise a slow
day/night light level; if the pad lamp is on (GPIO shim wrote the flag) we raise it so the tag stays
'visible', mirroring the real night-lamp behaviour."""
import math, os, time

class SpiDev:
    def __init__(self): self.max_speed_hz = 0
    def open(self, bus, dev): pass
    def xfer2(self, frame):
        t = time.time()
        lux = max(0.0, 512.0 * (0.5 + 0.5 * math.sin(t / 19.0)))   # 0..512 day/night
        sid = os.environ.get("STATION_ID", "STA1")
        try:
            if open(f"/tmp/airpost_lamp_{sid}").read().strip() == "1":
                lux = max(lux, 700.0)        # lamp on -> bright
        except OSError:
            pass
        d = max(0, min(1023, int(lux)))
        return [0, (d >> 8) & 0x03, d & 0xFF]
    def close(self): pass
