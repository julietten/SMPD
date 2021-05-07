# SMPD

Soil Moisture Profiling Device - the code for a device that collects soil moisture content, temperature, humidity, and rainfall that is transmitted over LoRaWAN to AWS to a Flask application displaying graphs of the data
This repository was developed for Case Western Reserve University's ECSE 399 senior project course. This project was developed by Juliette Naugle.

## Contents:


1. Folders, Files, and Descriptions
2. Software Prerequisites
4. Hardware Components
5. Microcontroller Pinouts


## 1. Folders, Files, and Descriptions:


### **STM32 Code**

**device_code.ino:** contains C++ code used for the STM32 to collect the data, connect to The Things Network, and transmit the data

### **AWS Lambda**

**lambda_function.py:** contains pPython code used in the Amazon Web Services Lambda function that took the transmission from the AWS MQTT Client and added it to a AWS DynamoDB Table

### **Flask**

**aws_controller.py:** contains Python code that made functions used to pull the data from the AWS DynamoDB table into arrays of data and sort functions to keep the data in timestamp order

**flask_app.py:** contains Python code that made the Flask application with graphs for each type of data - soil moisture content, temperature, humidity, and rainfall - and rendered different web pages based on how much time the user wanted to see, day, week, month, or all time

**templates/home.html:** contains the HTML code used to create the web pages with Chart.js code used to make the graphs for each data collected
