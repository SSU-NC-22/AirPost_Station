import paho.mqtt.client as mqtt #import the client
import time

broker_address="192.168.1.5" 
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
print("connecting to broker")

while 1:
     client.publish("house/bulbs/bulb1","OFF")