import json
from LEDActuator import LED


class Handler():
    def __init__(self):
        self.led = LED()

    def run(self, msg):
        msg = json.loads(msg.decode())
        if msg['value'] == 1:
            self.led.On()
        if msg['value'] == 0:
            self.led.Off()
