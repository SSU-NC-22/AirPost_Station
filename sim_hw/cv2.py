"""Minimal cv2 shim for station SITL: there is no clearance camera in simulation, so VideoCapture
reports 'not opened' and the station's TagSensor returns no detection (clearance unknown), which
run.py handles. On real hardware the genuine opencv + camera are used (this shim isn't on the path)."""
ROTATE_180 = 1; COLOR_BGR2GRAY = 6
class VideoCapture:
    def __init__(self, device=0): self._dev = device
    def isOpened(self): return False
    def read(self): return False, None
    def release(self): pass
def rotate(img, code): return img
def cvtColor(img, code): return img
