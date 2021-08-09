# AirPost_Station

AirPost_Station is a IOT platform based landing space for drone.

[TOC]

## Companion Computer

+ Raspberry Pi

## Sensors

+ USB-Port-GPS Module SKU:EZ-0048

  <img src="./README.assets/GpsSensor.png"  width="300"/>

  To specify station coordination through gps.

  [Wiki](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048)

  [Product Link](https://www.devicemart.co.kr/goods/view?no=1360762)

+ Raspberry Pi Camera Module V2

  <img src="./README.assets/RaspberryCam.png"  width="300"/>

  To measure cleaerence of landing space

  [Product Link](https://www.devicemart.co.kr/goods/view?no=1077951&gclid=CjwKCAjwi9-HBhACEiwAPzUhHM7rQAiEkU7HuskD-cf6QS4HtQLyge0wrAJ1CSpK6Mnv74iOIMtgExoCfRQQAvD_BwE)

+ DHT11 Temperature, Humid Sensor

  <img src="./README.assets/TempHumidSensor.png"  width="250"/>

  To measure status of landing space.

  [Product Link](https://www.alibaba.com/product-detail/DHT11-Temperature-and-Relative-Humidity-Sensor_60715089558.html)

+ Light Sensor

  <img src="./README.assets/LightSensor.png"  width="200"/>

  To measure light value of landing space. Sensor value used for actuating LED to ensure landing space visibility at night.

  [Product Link](https://www.amazon.com.au/YwRobot-Light-Sensor-Module-Photoresistor/dp/B07B47VVGY)

## Actuators

+ LED

  <img src="./README.assets/LEDModule.png"  width="300"/>

  [Product Link](https://www.devicemart.co.kr/goods/view?no=1384418)

## Communication Method

+ MQTT

  Between sink node server and station

+ GPIO

  Between companion computer and sensors

## Guide

+ Run

  + Publisher

    Gather sensor values and publish to the sink node server.

    `python3 run_pub.py`
    
  + Subscriber

    Get message from sink node server.

    `python3 run_sub.py`

+ Packages

  You can manually install all related packages with sensors. But through shell scripts in Requirements folder, it will be easier. Type bash ./install.sh in your terminal.

  ```
  cd Requirements
  sudo bash ./install.sh
  ```

+ GPS

  + Preparing

    1. install packages for GPS module.
       
       `sudo apt-get update && sudo apt-get -y install gpsd gpsd-clients python-gps`
       
       `pip3 install gps`
       
    2. Start the gpsd service and control it.

       Enable it: `sudo systemctl enable gpsd.socket`

       Start it: `sudo systemctl start gpsd.socket`

       Restart it: `sudo systemctl restart gpsd.socket`

       Check status: `sudo systemctl status gpsd.socket`

    3. Modify the configuration file of gpsd in /etc/default/gpsd
       Modify the "DEVICE" parameter according to the name of serial port in /dev folder.
       It is usually named "/dev/ttyUSB0" if you connect it to Raspberry Pi via USB cable.
       You can use "nano" or "vim.tiny" editor to finish it.

       <img src="./README.assets/Gpsconfig.jpg"  />

    4. Restart service:
       `sudo systemctl restart gpsd.socket`

       Finally, use this command to get information from GPS module.
       `sudo cgps -s`

  + Python example

    ```
    #! /usr/bin/python
    from gps import *
    import time
       
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
    print 'latitude\tlongitude\ttime utc\t\t\taltitude\tepv\tept\tspeed\tclimb' # '\t' = TAB to try and output the data in columns.
      
    try:
        while True:
            report = gpsd.next() #
    	    if report['class'] == 'TPV':
                    print  getattr(report,'lat',0.0),"\t",
                    print  getattr(report,'lon',0.0),"\t",
                    print getattr(report,'time',''),"\t",
                    print  getattr(report,'alt','nan'),"\t\t",
                    print  getattr(report,'epv','nan'),"\t",
                    print  getattr(report,'ept','nan'),"\t",
                    print  getattr(report,'speed','nan'),"\t",
                    print getattr(report,'climb','nan'),"\t"
                    time.sleep(1) 
    except (KeyboardInterrupt, SystemExit):      #when you press ctrl+c
        print "Done.\nExiting."
    ```

+ Camera

  + Preparing

    - Camset
      1. enable rasberry pi camera in `sudo raspi-config`
      2. `sudo vim /etc/modules` and add `bcm2835-v4l2` below

    + opencv-python

      1. install dependent packages

      2. ```
         sudo apt-get update && sudo apt-get upgrade -y
         sudo apt-get install build-essential cmake pkg-config -y
         sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev -y
         sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
         sudo apt-get install libxvidcore-dev libx264-dev -y
         sudo apt-get install libfontconfig1-dev libcairo2-dev -y
         sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev -y
         sudo apt-get install libgtk2.0-dev libgtk-3-dev -y
         sudo apt-get install libatlas-base-dev gfortran -y
         sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103 -y
         sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 -y
         sudo apt-get install python3-dev -y
         ```

      3. install opencv-python with pip3

         `sudo pip install opencv-contrib-python==4.1.0.25`

    + [apriltag](https://github.com/AprilRobotics/apriltag.git)

      ```
      cd Requirements/apriltag
      cmake .
      sudo make install
      ```

    + other packages

      ```
      pip install Cython
      pip install --upgrade imutils
      # Update pip
      python -m pip install -U pip
      # Install scikit-image
      python -m pip install -U scikit-image
      ```

  + Python example

    ```
    import cv2
    cap = cv2.VideoCapture(0) #0 or -1
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            cv2.imshow('camera', img)
            if cv2.waitKey(1) & 0xFF == 27: #esc
                break
        else:
            print('no camera!')
            break
    cap.release()
    cv2.destroyAllWindows()
    ```

+ Light Sensor

  + Preparing

    + py-spidev

      ```
      cd py-spidev/
      sudo python setup.py install
      ```

  + python Example

    ```
    import spidev
    import time
    
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz=500000
     
    def readChannel(channel):
      val = spi.xfer2([1,(8+channel)<<4,0])
      data = ((val[1]&3) << 8) + val[2]
      return data
    
    def ConvertVolt(data, places):
        volt = (data * 3.3)/float(1023)
        volt = round(volt, places)
        return volt
    
    if __name__ == "__main__":
      while(1):
        light_level = readChannel(0)
        light_volt = ConvertVolt(light_level, 2)
        print("Light Data : {} ({}V)".format(light_level, light_volt))
        time.sleep(0.5)
    ```

+ TempHumid Sensor

  + Prepareing

    + Adafruit_DHT

      ```
      sudo python3 -m pip install --upgrade pip setuptools wheel
      sudo pip3 install Adafruit_DHT
      ```

    + python board package

      `pip3 install board`

  + python Example

    ```
    import adafruit_dht
    from board import *
    import time
    
    # GPIO18
    SENSOR_PIN = D18
    
    dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
    
    while True:
        time.sleep(1)
        try:
            temperature = dht11.temperature
            humidity = dht11.humidity
        except:
            continue
            
        print(f"Humidity= {humidity:.2f}")
        print(f"Temperature= {temperature:.2f}°C")
    ```

    

+ MQTT client

  + mosquitto-client python

    ```
    sudo apt-get install build-essential libc-ares-dev uuid-dev libssl-dev libcurl4-openssl-dev libmysqlclient-dev
    sudo apt-get install mosquitto-clients
    pip3 install paho-mqtt
    ```

  + Python example

    + Publisher

      ```
      import random
      import time
      import json
      import datetime
      
      from paho.mqtt import client as mqtt_client
      
      broker = '192.168.1.5'
      port = 1883
      topic = "/data/station"
      client_id = 'P0000001'
      
      msgs = [{
          "message" : "hello"
      }]
      
      def connect_mqtt():
          def on_connect(client, userdata, flags, rc):
              if rc == 0:
                  print("Connected to MQTT Broker!")
              else:
                  print("Failed to connect, return code %d\n", rc)
      
          client = mqtt_client.Client(client_id)
          client.on_connect = on_connect
          client.connect(broker, port)
          return client
      
      
      def publish(client):
          while True:
              time.sleep(1)
              msg = json.dumps(msgs)
              result = client.publish(topic, msg)
              # result: [0, 1]
              status = result[0]
              if status == 0:
                  print(f"Send msg to topic `{topic}`")
              else:
                  print(f"Failed to send message to topic {topic}")
      
      
      def run():
          client = connect_mqtt()
          client.loop_start()
          publish(client)
      
      
      if __name__ == '__main__':
          run()
      ```

      

    + Subscriber

      ```
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
      ```

      

## Reference Link

- [Gps Wiki](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048)
- [Raspberry Pi Camera Setting](http://www.3demp.com/community/boardDetails.php?cbID=236)

- [Opencv raspberry pi camera streaming](https://blog.xcoda.net/98)
- [LightSensor ADC setting](https://tutorials-raspberrypi.com/infrared-distance-measurement-with-the-raspberry-pi-sharp-gp2y0a02yk0f/)
- [mosquitto installation](https://wnsgml972.github.io/mqtt/2018/02/13/mqtt_ubuntu-install/)
- [pqho-mqtt installation](https://developer-finn.tistory.com/1)

