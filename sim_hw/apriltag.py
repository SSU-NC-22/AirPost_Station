"""Simulated apriltag so `from apriltag import apriltag` imports in SITL. With no real camera the
station's TagSensor.read path returns 'no detection' (clearance unknown), which run.py handles."""
class apriltag:
    def __init__(self, family="tag36h11"): self.family = family
    def detect(self, image): return []
