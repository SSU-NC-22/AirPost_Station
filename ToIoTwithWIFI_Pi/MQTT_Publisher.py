import datetime
import json
import time

from paho.mqtt import client as mqtt_client

from Sensors.GPSSensor import GPSSensor
from Sensors.LightSensor import LightSensor
from Sensors.TagSensor import TagSensor
from Sensors.TempHumidSensor import TempHumidSensor


class Publisher:
	def __init__(self):
		self.broker = '192.168.1.5'
		self.port = 1883
		self.topic = "/data/station"
		self.client_id = 'sta00001'
		self.client = mqtt_client.Client(self.client_id)

	def connect_mqtt(self):
		def on_connect(client, userdata, flags, rc):
			if rc == 0:
				print("Connected to MQTT Broker!")
			else:
				print("Failed to connect, return code %d\n", rc)

		self.client.on_connect = on_connect
		self.client.connect(self.broker, self.port)

	def loop_start(self):
		self.client.loop_start()

	def publish(self, msgs):
		msg = json.dumps(msgs)
		result = self.client.publish(self.topic, msg)
		# result: [0, 1]
		status = result[0]
		if status == 0:
			print(f"Send msg to topic `{self.topic}`")
		else:
			print(f"Failed to send message to topic {self.topic}")


if __name__ == '__main__':
	publisher = Publisher()
	publisher.connect_mqtt()
	publisher.loop_start()

	gps = GPSSensor()
	tag = TagSensor()
	light = LightSensor()
	temp_humid = TempHumidSensor()

	while True:
		time.sleep(1)
		msgs = [{
			"sensor_id": 0,
			"node_id": publisher.client_id,
			"values": {
				"temp": temp_humid.ReadTemperature(),
				"light": light.Read()[0],
				"humid": temp_humid.ReadHumidity(),

				"lat": gps.Read()['lat'],
				"lon": gps.Read()['lon'],
				"alt": gps.Read()['alt'],

				"clear": tag.Read()[0],
				"status": 0,
			},
			"timestamp": str(datetime.datetime.now())
		}]

		publisher.publish(msgs)
