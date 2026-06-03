"""Simulated gpsd client for SITL. The real GPSSensor calls gps(...).next() and reads a TPV report's
lat/lon/alt. We return the station's known position (STATION_LAT/LON/ALT env, set from the world)."""
import os
WATCH_ENABLE = 1; WATCH_NEWSTYLE = 2

class _Report(dict):
    def __init__(self):
        super().__init__()
        self["class"] = "TPV"
        self.lat = float(os.environ.get("STATION_LAT", "37.5"))
        self.lon = float(os.environ.get("STATION_LON", "127.0"))
        self.alt = float(os.environ.get("STATION_ALT", "0.0"))
        self.time = None; self.epv = None; self.ept = None
        self.speed = 0.0; self.climb = 0.0

class gps:
    def __init__(self, mode=0): pass
    def next(self): return _Report()
