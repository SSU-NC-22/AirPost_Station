#include "ToIoTwithWIFI.h"
#include <cstring>
#include <stdarg.h>
#include "arduino.h"
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

ToIoTwithWIFI::ToIoTwithWIFI()
{
    PubSubClient* client2 = new PubSubClient (espClient);
    client = *client2;
}

void ToIoTwithWIFI::setupToIoTwithWIFI(char* nodeI, char* ssid, char* password, char* broker_ip, int broker_port)
{
    Serial.begin(115200);
    
    delay(500);
   
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
 
    nodeId = nodeI;
    snprintf(topic, 26, "data/%s", nodeId);

    client.setServer(broker_ip, broker_port);
}

void ToIoTwithWIFI::reconnect()
{
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP8266Client")) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void ToIoTwithWIFI::pub(char* sensorId, int cnt, ...)
{
    if(!client.connected())
    {
        reconnect();
    }
    va_list ap;
    va_start(ap, cnt);
    int res = 0;
    memset(msg, 0, 50);
    res = sprintf(msg, "%s,", sensorId);
    for(int i=0; i<cnt; i++)
    {
        if(i == cnt-1)
        {
            res += vsprintf(msg+res, "%lf", ap);
        }
        else
        {
            res += vsprintf(msg+res, "%lf,", ap);
        }
        va_arg(ap, double);
    }
    va_end(ap);
    Serial.print("[Pub] ");
    Serial.print(topic);
    Serial.print(":");
    Serial.println(msg);
    client.publish(topic,  msg);

}