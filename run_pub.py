from MQTT_Connection.MQTT_Publisher import MQTTPublisher
from Sensors.GPSSensor import GPSSensor
from Sensors.LightSensor import LightSensor
from Sensors.TagSensor import TagSensor
from Sensors.TempHumidSensor import TempHumidSensor

publisher = MQTTPublisher()
gps = GPSSensor()
tag = TagSensor()
light = LightSensor()
temp_humid = TempHumidSensor()


publisher.connect_mqtt()
publisher.loop_start()

while True:
		temp_humid.Read()
		gps.Read()
		light.Read()
		tag.Read()

		msgs = [{
			"sensor_id": 0,
			"node_id": publisher.client_id,
			"values": {
				"temp": temp_humid.temperature,
				"light": light.data,
				"humid": temp_humid.humidity,

				"lat": gps.data['lat'],
				"lon": gps.data['lon'],
				"alt": gps.data['alt'],

				"clear": len(tag.detectedTags),
				"status": 0,
			},
			"timestamp": str(datetime.datetime.now())
		}]

		print(msgs)
		publisher.publish(msgs)

		