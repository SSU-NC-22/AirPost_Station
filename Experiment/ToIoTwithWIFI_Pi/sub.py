
from paho.mqtt import client as mqtt_client

broker = '192.168.1.5'
port = 1883
topic = "/data/station"
client_id = 'S0000001'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received msg from `{msg.topic}` topic")
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print(m_decode)
        
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()