# IoT-SmartGarden
### _Semester project for Internet of Things lab class_

![Build Status](https://ci.appveyor.com/api/projects/status/%7B%7Bstatus_id%7D%7D)

## About this project
The goal of this project is to create an iot device which will be reliable in order to water garden plants when humidity of the soil is low.
Also provide information about air temperature, air humidity and water tank level.


## Hardware Prerequisites

- Raspberry Pi Zero W
- Soil Hygrometer sensor
- Distance sensor (HC-SR04)
- 330Ω and 470Ω Capacitors
- Temperature-Humidity Sensor (DHT11)
- 12V PSU
- 12V pump
- 3.3V Relay
- Water tank reservoir
- Gmail Account with 2 factor Authenication

You have to generate an app password from [here](https://myaccount.google.com/apppasswords) in order to put it in the code as your email password.

Also you will need a soldering iron, some jumper cables and silicon tubes for the water pump.

The connection diagram can be found [here](https://github.com/NikosX1/IoT-SmartGarden/blob/main/diagrams/PI-DIAGRAM.pdf).



## Installation
1. Connect to Pi Zero via SSH
2. Clone this repo:`https://github.com/NikosX1/IoT-SmartGarden`
3. In file waterPlant.py you have to put your email credentials (username/app-password) in the lines 14,15.
4. sudo chmod +x waterPlant.py
5. Finally execute crontab -e and add the bottom line: * * * * * /path_to_program/Iot-SmartGarden/waterPlant.py 

### Info
 
 Class: Internet of Things</br>
 Author: ΝΙΚΟΛΑΟΣ ΧΡΟΝΟΠΟΥΛΟΣ ΑΜ:131094</br>
 Semester: Fall 2021</br></br>
 
 University of West Attica</br>
 Department of Informatics and Computer Engineering
