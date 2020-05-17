# FYP - Automated Data Collecting System for Environment Using UAVs and Smartphones

IVE(LWL), Software Engineering, Final Year Project

## Collaborators

* **Siu Chi Wang** - *Initial work* - [wing199901](https://github.com/wing199901)
* **Siu Chi Wang** - *Initial work* - [wing199901](https://github.com/wing199901)
* **Siu Chi Wang** - *Initial work* - [wing199901](https://github.com/wing199901)
* **Siu Chi Wang** - *Initial work* - [wing199901](https://github.com/wing199901)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Hardware

```
1. a Raspberry Pi 3B+
2. a Navio2 Autopilot HAT
3. a high power wireless USB adapter(Alfa AWUS036NHA)
4. a DIY quadcopter
5. a 4s battery
6. a laptop
7. a Smartphone
8. DHT22 sensor
9. SDS011 sensor
```

Software

```
1. Python3(3.8) 
2. QGroundControl
3. Mission Planner
4. Terminal
```

## Installing
### Raspberry Pi Configuration
Navio requires a preconfigured Raspbian to run. Emlid provide a unified SD card image for Raspberry Pi.

Follow the instruction to configure your Raspberry Pi
(https://docs.emlid.com/navio2/common/ardupilot/configuring-raspberry-pi/)

```
If you want to use SSH to remote access your Raspberry Pi, placing a file named 'ssh' into the boot partition.
```

#### Configure Access Point(AP)
We choose to use create_ap to create an access point, because it provides a simple way to do thing easier.

```
git clone https://github.com/oblique/create_ap
cd create_ap
make install
```

The basic syntax to create a NATed virtual network is the following:

```
create_ap wlan0 eth0 MyAccessPoint MyPassPhrase
```

Here is our configuration

```
CHANNEL=default
GATEWAY=192.168.12.1
WPA_VERSION=1+2
ETC_HOSTS=0
DHCP_DNS=gateway
NO_DNS=0
NO_DNSMASQ=0
HIDDEN=0
MAC_FILTER=0
MAC_FILTER_ACCEPT=/etc/hostapd/hostapd.accept
ISOLATE_CLIENTS=0
SHARE_METHOD=none
IEEE80211N=1
IEEE80211AC=0
HT_CAPAB=[HT40+]
VHT_CAPAB=
DRIVER=nl80211
NO_VIRT=0
COUNTRY=
FREQ_BAND=2.4
NEW_MACADDR=
DAEMONIZE=0
NO_HAVEGED=0
WIFI_IFACE=wlan0
INTERNET_IFACE=
SSID=Navio
PASSPHRASE=ChangeMe
USE_PSK=0
```

To run this configuration with:

```
create_ap --config /etc/create_ap.conf
```

Start service immediately:

```
systemctl start create_ap
```

Start on boot:

```
systemctl enable create_ap
```
### UAV Configuration
#### ArduPilot Configuration
We run ArduPilot on Raspberry Pi with Navio. The autopilot's code works directly on Raspberry Pi.

You can follow the instructions with the Navio2 docs(https://docs.emlid.com/navio2/common/ardupilot/installation-and-running/)

#### Onboard calibration
Here we use Mission Planner to calibrate the onboard sensors.

Follow the instruction to calibrate the onboard sensors
(https://docs.emlid.com/navio2/ardupilot/tips/)

### Sensors
In this project, we choose two sensors that install on the UAV and transmit the climate date to laptop

#### DHT22 temperature-humidity sensor
The DHT22 is a basic, low-cost digital temperature and humidity sensor. It uses a capacitive humidity sensor and a thermistor to measure the surrounding air, and spits out a digital signal on the data pin

![image](https://5.imimg.com/data5/DV/AL/GJ/SELLER-6366772/dht22-digital-temperature-and-humidity-sensor-module-500x500.jpg)

* We use the GPIO17_DF13 as the data pin
* Pin 2 for 5V
* Pin 6 for ground

![image](https://docs.emlid.com/navio2/dev/img/pinout.png)

#### SDS011 Air Quality Sensor
SDS sensor is connected through a USB-Serial-Converter,


## Built With

* [DroneKit Python](https://github.com/dronekit/dronekit-python) - The drone api used
* [QGroundControl](http://qgroundcontrol.com) - The ground control station used on smartphone
* [Navio2](https://emlid.com/navio/) - Autopilot HAT for Raspberry Pi Powered by ArduPilot and ROS used
* [create_ap](https://github.com/oblique/create_ap) - 



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

