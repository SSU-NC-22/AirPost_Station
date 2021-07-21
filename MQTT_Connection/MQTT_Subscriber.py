from paho.mqtt import client as mqtt_client


class MQTTSubscriber():
	def __init__(self):
		self.broker = '192.168.1.6'
		self.port = 1883
		self.topic = "/data/station"
		self.client_id = 'sta00000'
		self.client = mqtt_client.Client(self.client_id)


	def connect_mqtt(self):
		def on_connect(client, userdata, flags, rc):
			if rc == 0:
				print("Connected to MQTT Broker!")
			else:
				print("Failed to connect, return code %d\n", rc)

		self.client.on_connect = on_connect
		self.client.connect(self.broker, self.port)


	def subscribe(self):
		def on_message(client, userdata, msg):
			print(f"Received msg from `{msg.topic}` topic")
            result = json.loads(json_data)
			m_decode = str(msg.payload.decode("utf-8", "ignore"))
			print(m_decode)

		self.client.subscribe(self.topic)
		self.client.on_message = on_message
	
	def loop_forever(self):
		self.client.loop_forever()
