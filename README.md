# AirPost_Station — the smart landing pad (IoT)

This repository is a **landing station** in the [AirPost](https://github.com/jsoone24/NC_AirPost)
drone-delivery system: the physical helipad a drone takes off from and lands on, made "smart" by a
Raspberry Pi and a handful of sensors.

## What it is, in plain terms

A station is a small **always-on IoT device** sitting under a helipad with an AprilTag marker. Its job
is to make the pad *known, safe, and landable* at any time:

- **Knows where it is** — a GPS module reports the pad's exact coordinates, so the backend can route
  drones to it (no hardcoded map).
- **Knows its condition** — temperature, humidity and a light sensor report the pad's environment.
- **Stays landable at night** — when the light sensor reads "dark", the station turns on a **pad LED
  (lamp)** so the drone's downward camera can still see the AprilTag and precision-land. This is the
  station's key trick: vision landing needs light, so the pad provides its own.
- **Checks clearance** — a Pi camera can verify the landing space is clear.

## Where it sits in AirPost

```
AirPost_Station (Raspberry Pi)
  ├─ GPS, temp, humidity, light  ──MQTT──► Sink ──► Kafka ──► backend (map + dashboards)
  └─ light sensor "dark?" ──► turn ON pad LED ──► drone camera can read the AprilTag at night
```

The station continuously **publishes its sensors over MQTT**; the [Sink](https://github.com/SSU-NC-22/AirPost_Sink)
forwards them to Kafka, and the backend stores/charts them and shows the station on the live map. The
night-lamp rule is driven by the light reading (locally and/or via the backend's logic engine).

> In the [simulation](https://github.com/jsoone24/NC_AirPost/tree/main/simulation), `station_iot.py`
> plays this exact role: each station self-registers with the backend and streams GPS/temp/humidity/
> light, raising a virtual pad lamp in the dark — so the simulated world behaves like these real boards.

The rest of this README is the **hardware list and the Raspberry-Pi bring-up** (wiring and installing
the GPS, camera, DHT11, light sensor, LED, and the MQTT client).

---


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
  + type following command ```python3 run.py```

+ Packages

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

  + Preparing

    + py-spidev

      ```
      cd py-spidev/
      sudo python setup.py install
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


+ MQTT client

  + mosquitto-client python

    ```
    sudo apt-get install build-essential libc-ares-dev uuid-dev libssl-dev libcurl4-openssl-dev libmysqlclient-dev
    sudo apt-get install mosquitto-clients
    pip3 install paho-mqtt
    ```
      

## Reference Link

- [Gps Wiki](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048)
- [Raspberry Pi Camera Setting](http://www.3demp.com/community/boardDetails.php?cbID=236)

- [Opencv raspberry pi camera streaming](https://blog.xcoda.net/98)
- [LightSensor ADC setting](https://tutorials-raspberrypi.com/infrared-distance-measurement-with-the-raspberry-pi-sharp-gp2y0a02yk0f/)
- [mosquitto installation](https://wnsgml972.github.io/mqtt/2018/02/13/mqtt_ubuntu-install/)
- [pqho-mqtt installation](https://developer-finn.tistory.com/1)

