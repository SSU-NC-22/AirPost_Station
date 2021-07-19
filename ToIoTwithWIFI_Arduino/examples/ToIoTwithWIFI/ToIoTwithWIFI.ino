#include "ToIoTwithWIFI.h"
#include "config.h"

double value = 0.0; 
ToIoTwithWIFI t;

void setup() {
  t.setupToIoTwithWIFI(nodeId, ssid, password, mqtt_server, mqtt_port);
}


void loop() {
  t.pub("sensor-uuid-1", 1, value);
  t.pub("sensor-uuid-2", 2, value, value);
  t.pub("sensor-uuid-3", 3, value, value, value);
  delay(4000);
  value+=0.1; // sensor value
  
}
