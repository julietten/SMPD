#include <lmic.h>
#include <hal/hal.h>
#include <DHT.h>
#include <CayenneLPP.h>

//defining pin connections
#define loraSCK PA5 //lora radio transceiver SCK pin
#define loraMISO PA6 //lora radio transceiver MISO pin
#define loraMOSI PA7 //lora radio transceiver MOSI pin
#define loraNSS  PA4//lora radio transceiver NSS pin
#define loraRST PB0 //lora radio transceiver NRESET pin
#define loraG0 PA3 //lora radio transceiver G0 pin
#define loraG1 PB5 //lora radio transceiver G1 pin
#define soilOut PB1 //soil analog output pin
#define dhtOut PA0 //dht11 output pin
#define rainOut PA1 //rain water gauge output pin

#define DHTTYPE DHT11 //sets dht type as dht11

static const u1_t PROGMEM APPEUI[8]={ 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx }; //app eui in litle endian format
static const u1_t PROGMEM DEVEUI[8]={ 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx }; //dev eui in little endian format
static const u1_t PROGMEM APPKEY[16] = { 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx, 0xxx }; //app key in big endian format

void os_getArtEui(u1_t* buf){memcpy_P(buf, APPEUI, 8);}
void os_getDevEui(u1_t* buf){memcpy_P(buf, DEVEUI, 8);}
void os_getDevKey(u1_t* buf){memcpy_P(buf, APPKEY, 16);}

CayenneLPP lpp(51); //stores object of cayenneLPP class that encodes data
static osjob_t sendjob;
const unsigned TX_INTERVAL = 1200; //uplink frequency
DHT dht(dhtOut, DHTTYPE); //init dht sensor
volatile int tips = 0; //stores the number of rainwater tips over the duration of the sleep mode to calculate rainfall

//sets the pins of the LoRa radio transceiver for lmic library
const lmic_pinmap lmic_pins = { 
  .nss = loraNSS, //slave select
  .rxtx = LMIC_UNUSED_PIN, //not used
  .rst = loraRST, //reset transceiver
  .dio = {loraG0, loraG1, LMIC_UNUSED_PIN}, //status information
};

/* event handler for device's connection to network */
void onEvent(ev_t ev){
  switch(ev){
    case EV_JOINING:
      Serial.println("joining");
      break;
    case EV_JOINED:
      Serial.println("joined");
      break;
    case EV_JOIN_FAILED:
      Serial.println("join failed");
      break;
    case EV_TXCOMPLETE:
      Serial.println("txcomplete");
      os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
      break;
    default:
      break;
  }
}

//function used to print cayennelpp transmission
void printHex(uint8_t num) {
  char hexCar[2];

  sprintf(hexCar, "%02X", num);
  Serial.print(hexCar);
}

/* function the determines the average of a data value based on three data collections
 * param: integer to determine which data is being averaged
 * return: the average of three values */
float dataAvg(int val){
  float data = 0; //stores value of the averaged data
  for(unsigned int i = 0; i < 3; i++){
    if(val == 1)
      data += map(analogRead(soilOut), 0, 1023, 0, 100);
    if(val == 2)
      data += dht.readTemperature(true);
    if(val == 3)
      data += dht.readHumidity();
  }
  return data/3;
}

/* function that records the rain gauge tips
 * param: the amount of time spent in sleep mode in milliseconds */
void sleepTips(int duration){
  tips = 0; //resets the rainwater tips for the next period's recording
  int numLoops = duration / 500;
  int i = 0;
  while(i <= numLoops){
    if (digitalRead(rainOut) == HIGH)
      tips++;
    delay(500);
    i++;
  }
}

/* function that sends the soil content data encoded with CayenneLPP over LoRaWAN */
void do_send(osjob_t* job){
  if(LMIC.opmode & OP_TXRXPEND){ //checks that data is able to transmit
    Serial.println("error: won't send");
  }else{

    sleepTips(600000);
    
    float soil_content = dataAvg(1); //stores the average of 3 data collections of soil moisture
    float temp = dataAvg(2); //stores the average of 3 data collections of temperature
    float humidity = dataAvg(3); //stores the average of 3 data collections of humidity
    float inch_rain_hr = (tips * 1.5 / 16.3871) * 6; //calculates rain water per hour in inches

    lpp.reset(); //resets so previous payload isn't included in new payload
    
    lpp.addAnalogOutput(1, soil_content); //adds the soil moisture value to the cayenneLLP encoded data being sent
    lpp.addRelativeHumidity(2,humidity); //adds the humidity value to the cayenneLLP encoded data being sent
    lpp.addTemperature(3,temp); //adds the temp value to the cayenneLLP encoded data being sent
    lpp.addAnalogOutput(4, inch_rain_hr); //adds the soil moisture value to the cayenneLLP encoded data being sent

    //loop that prints the packet sent over LoRaWAN
    for(unsigned int i=0; i< lpp.getSize(); i++) {
      printHex(lpp.getBuffer()[i]);
    }
    Serial.println("");
    
    LMIC_setTxData2(1, lpp.getBuffer(), lpp.getSize(), 0); //sends the cayenneLPP encoded data
  }
}
  
void setup(){

  pinMode(soilOut, OUTPUT); //sets soil pin pinmode to output
  pinMode(rainOut, INPUT_PULLUP); //sets rainwater gauge pin as input pullup

  Serial.begin(115200); //allows for printing values to serial monitor
  os_init(); //initializes lmic library
  LMIC_reset(); //resets session
  dht.begin(); //initializes dht library

  LMIC_setDrTxpow(DR_SF7, 14); //sets spreading factor and dbi
  LMIC_selectSubBand(1); //sets transmissions to us subband
  
  do_send(&sendjob); //sends uplink
}

void loop(){
  os_runloop_once();
}
