# SMPD

### Soil Moisture Profiling Device - the code for a device that collects soil moisture content, temperature, humidity, and rainfall that is transmitted over LoRaWAN to AWS to a Flask application displaying graphs of the data
### This repository was developed for Case Western Reserve University's ECSE 399 senior project course. This project was developed by Juliette Naugle.

## Device:

![20210419_145709_HDR_2](https://user-images.githubusercontent.com/9967479/117495410-93118280-af43-11eb-9d45-81a6962239f3.jpg)


## Flask Application:

![flask_app_april19](https://user-images.githubusercontent.com/9967479/117495028-21d1cf80-af43-11eb-892d-0b71392cb5dd.JPG)


## Contents:


1. Folders, Files, and Descriptions
2. Software Prerequisites
3. Hardware Components
4. Microcontroller Pinouts


## 1. Folders, Files, and Descriptions:


### **STM32 Code**

**device_code.ino:** contains C++ code used for the STM32 to collect the data, connect to The Things Network, and transmit the data

### **AWS Lambda**

**lambda_function.py:** contains Python code used in the Amazon Web Services Lambda function that took the transmission from the AWS MQTT Client and added it to a AWS DynamoDB Table

### **Flask**

**aws_controller.py:** contains Python code that made functions used to pull the data from the AWS DynamoDB table into arrays of data and sort functions to keep the data in timestamp order

**flask_app.py:** contains Python code that made the Flask application with graphs for each type of data - soil moisture content, temperature, humidity, and rainfall - and rendered different web pages based on how much time the user wanted to see, day, week, month, or all time

**templates/home.html:** contains the HTML code used to create the web pages with Chart.js code used to make the graphs for each data collected


## 2. Software Prerequisites:


### **For the STM32 code:**

LMIC library, CayenneLPP library, DHT library


### **For the Flask code:**

Flask, json, datetime, boto3, chart.js


### **For the AWS Lambda function:**

boto3, json


### **Other software configurations:**

For the device to communicate with the Helium console, an account and access keys for the Helium Console is needed and the access keys need to be directly added to the device_code.ino file in little endian and big endian format as directed.

For the data to be sent from the Helium console to the Amazon Web Servies MQTT Client, an AWS integration needs to be added to the Helium console. An AWS account must be created and also an IAM user with the correct permissions must be made so that the access keys from the IAM user can be added to the Helium Console / AWS integration.

The AWS Lambda function must be set to trigger from the MQTT Client receiving messages using an IoT Core Rule.

The AWS DynamoDB Table must be given permissions to allow the Lambda function to add data to it.


## 3. Hardware Components:

STM32 Blue Pill microcontroller, LoRa radio, capacitive soil moisture sensor, DHT11 temperature and humidity sensor, tipping bucket rainwater gauge using a magnetic switch, 10 kOhm pull up resistor for the rainwater gauge, battery holder, and a waterproof case for the device.


## 4. Microcontroller Pinouts:

Based on the pins of the STM32 Blue Pill

### **LoRa radio connections:**
SCK to PA5, MISO to PA6, MOSI to PA7, NSS to PA4, RST to PB0, G0 to PA3, G1 to PB5, GND to GND, VIN to 3.3V

### **Capacitive soil moisture sensor connections:**
AOUT to PB1, GND to GND, VCC to 3.3V

### **DHT11 temperature and humidity sensor connections:**
DATA to PA0, GND to GND, VCC to 5V

### **Rainwater gauge magnetic switch connections:**
Data pin to PA1 with a 10 kOhm pull up resistor, GND to GND
