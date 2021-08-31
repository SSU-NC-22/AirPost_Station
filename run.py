from MQTT_Connection.MQTT_Connection import MQTT
from Actuator.Handler import Handler
from Sensors.GPSSensor import GPSSensor
from Sensors.LightSensor import LightSensor
from Sensors.TagSensor import TagSensor
from Sensors.TempHumidSensor import TempHumidSensor
from datetime import datetime
import time
import json

broker = '58.230.119.87'
port = 9708
client_id = '0'


gps = GPSSensor()
tag = TagSensor()
light = LightSensor()
temp_humid = TempHumidSensor()


handler = Handler()
mqtt = MQTT(broker, port, client_id)
mqtt.connect_mqtt()
mqtt.subscribe("data/0", handler)
#mqtt.subscribe("command/downlink/ActuatorReq/0", handler)


while True:
	if temp_humid.Read() == -1:
		print("temp_humid read fail")
	if gps.Read() == -1:
		print("gps read fail")
	if light.Read() == -1:
		print("light read fail")
	if tag.Read() ==-1:
		print("tag read fail")
		clear = None
	else:
		len(tag.detectedTags)
	
	msgs = {
		"node_id": client_id,
		"values": {
			"temp": temp_humid.temperature,
			"humid": temp_humid.humidity,
			"light": light.data,

			"lat": gps.data['lat'],
			"lon": gps.data['lon'],
			"alt": gps.data['alt'],

			"clear": clear,
			"status": 0,
		},
		"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	}
	
	msg = json.dumps(msgs)

	mqtt.publish("data/0", msg)
	print("publish: ", type(msg), msg, "\n")

	time.sleep(1)
