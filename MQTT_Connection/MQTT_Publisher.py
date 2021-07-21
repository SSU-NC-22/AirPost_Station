import datetime
import json
import time

from paho.mqtt import client as mqtt_client

class MQTTPublisher():
	def __init__(self):
		self.broker = '192.168.1.6'
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

	def publish(self, msgs):
		msg = json.dumps(msgs)
		result = self.client.publish(self.topic, msg)
		# result: [0, 1]
		status = result[0]
		if status == 0:
			print(f"Send msg to topic `{self.topic}`")
		else:
			print(f"Failed to send message to topic {self.topic}")

	def loop_start(self):
		self.client.loop_start()