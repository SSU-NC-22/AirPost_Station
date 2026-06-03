"""Simulated RPi.GPIO for running the real AirPost_Station code off a Raspberry Pi (SITL).
Implements only what the station uses (LED actuator). Writes the pad-lamp state to
/tmp/airpost_lamp_<STATION_ID> so the Gazebo world's pad light can mirror it — exactly what the
real GPIO pin would drive. When real hardware arrives, this shim is simply not on the path."""
import os

BCM = "BCM"; BOARD = "BOARD"; OUT = "OUT"; IN = "IN"; HIGH = 1; LOW = 0
_state = {}

def setwarnings(_): pass
def setmode(_): pass
def setup(pin, mode, initial=LOW): _state[pin] = initial
def cleanup(*a): _state.clear()
def output(pin, value):
    _state[pin] = value
    sid = os.environ.get("STATION_ID", "STA1")
    try:
        open(f"/tmp/airpost_lamp_{sid}", "w").write("1" if value else "0")
    except OSError:
        pass
def input(pin): return _state.get(pin, LOW)
