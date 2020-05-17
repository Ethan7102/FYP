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
3. a high power wireless USB adapter
4. a DIY quadcopter
5. a 4s battery
6. a laptop
7. a Smartphone
8. DHT22 sensor
9. SDS011 sensor
```

Software

```
1. Python3 
2. QGroundControl
3. Terminal
```

## Installing
### Raspberry Pi Configuration
Navio requires a preconfigured Raspbian to run. Emlid provide a unified SD card image for Raspberry Pi.

Follow the instruction to configure your Raspberry Pi
(https://docs.emlid.com/navio2/common/ardupilot/configuring-raspberry-pi/)

#### Configure Access Point(AP)
We choose to use create_ap to create an access point, because it provides a simple way to do thing easier.

```
git clone https://github.com/oblique/create_ap
cd create_ap
make install
```

Test
```

```
## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

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

