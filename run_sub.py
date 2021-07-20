from MQTT_Connection.MQTT_Subscriber import MQTTSubscriber

subscriber = MQTTSubscriber()
subscriber.connect_mqtt()
subscriber.subscribe()
subscriber.loop_forever()