#ifndef ToIoTwithWIFI_H
#define ToIoTwithWIFI_H

#include "arduino.h"
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


class ToIoTwithWIFI
{
    public:
        ToIoTwithWIFI();
        void setupToIoTwithWIFI(char* nodeI, char* ssid, char* password, char* broker_ip, int broker_port);
        void pub(char* sensorId, int cnt, ...);
        void reconnect();
        PubSubClient client;
    private:
        unsigned long lastMsg = 0;
        char topic[26];
        char msg[50];  
        char* nodeId;
        WiFiClient espClient;
        
};

#endif