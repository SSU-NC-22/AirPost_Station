from paho.mqtt import client as mqtt_client
from Actuator.Handler import Handler
from Sensors.GPSSensor import GPSSensor
from Sensors.LightSensor import LightSensor
from Sensors.TagSensor import TagSensor
from Sensors.TempHumidSensor import TempHumidSensor
from datetime import datetime
import time
import json


class MQTT():
    def __init__(self, broker, port, client_id):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.client = mqtt_client.Client(self.client_id)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, topic, msg):  # input msg type : string
        self.pub_topic = topic
        result = self.client.publish(self.pub_topic, msg)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send msg to topic `{self.pub_topic}`")
        else:
            print(f"Failed to send message to topic {self.pub_topic}")

    def subscribe(self, topic, handler):
        self.sub_topic = topic
        self.handler = handler

        def on_message(client, userdata, msg):  # return msg.payload
            print(f"Received msg from `{msg.topic}` topic")
            self.handler.run(msg.payload)

        self.client.on_message = on_message
        self.client.subscribe(self.sub_topic)


if __name__ == "__main__":
    broker = '58.230.119.87'
    port = 9708
    client_id = 'STA0'

    gps = GPSSensor()
    tag = TagSensor()
    light = LightSensor()
    temp_humid = TempHumidSensor()

    handler = Handler()
    mqtt = MQTT(broker, port, client_id)
    mqtt.connect_mqtt()
    mqtt.subscribe("command/downlink/ActuatorReq/"+client_id)

    while True:
        # sensor value exception handler
        if temp_humid.Read() == -1:
            print("temp_humid read fail")
        if gps.Read() == -1:
            print("gps read fail")
        if light.Read() == -1:
            print("light read fail")
        if tag.Read() == -1:
            print("tag read fail")
            clear = None
        else:
            clear = len(tag.detectedTags)

        msgs = {
            "node_id": client_id,
            "values": [
                temp_humid.temperature,
                temp_humid.humidity,
                light.data,

                gps.data['lat'],
                gps.data['lon'],
                gps.data['alt'],

                clear
            ],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        msg = json.dumps(msgs)
        mqtt.publish("data/"+client_id, msg)
        print("publish: ", type(msg), msg, "\n")

        time.sleep(1)
