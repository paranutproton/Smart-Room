#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "Adafruit_SGP30.h"
#include <Wire.h>
using namespace std;
#define WIFI_STA_NAME "Gear26"
#define WIFI_STA_PASS  "0819719988"
#define MQTT_SERVER   "broker.hivemq.com"
#define MQTT_PORT     1883
#define MQTT_USERNAME "esp8266"
#define MQTT_PASSWORD "okokay1234"
#define MQTT_NAME     "esp8266"
WiFiClient client;
PubSubClient mqtt(client);
int num=0;
Adafruit_SGP30 sgp;
#define Vibrator D6
int motion_detected = LOW;
char msg[10];
char msg1[10];
char msg2[10];
char msg3[10];
char msg_all[50];
String s;
int SENSOR_OUTPUT_PIN = 14;

uint32_t getAbsoluteHumidity(float temperature, float humidity) {
    // approximation formula from Sensirion SGP30 Driver Integration chapter 3.15
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
    return absoluteHumidityScaled;
}

void setup() {
 Serial.begin(115200);
 WiFi.mode(WIFI_STA);
 pinMode(SENSOR_OUTPUT_PIN, INPUT); 
 while (!Serial) ; 
  delay(250);
  Serial.println(WIFI_STA_NAME); 
  Serial.println("WIFI Connecting");
  WiFi.begin(WIFI_STA_NAME, WIFI_STA_PASS);
 while (num<20) {
  delay(500);
  Serial.print(".");
  num++;
 }
 if (WiFi.status() == WL_CONNECTED) {
  Serial.print("\n WiFi Connected. \n");
 }else{
  Serial.print("\n WIFI Connect fail. ");
 }
 if (! sgp.begin()){
     Serial.println("Sensor not found :(");
     while (1);
     }
     Serial.print("Found SGP30 serial #");
     Serial.print(sgp.serialnumber[0], HEX);
     Serial.print(sgp.serialnumber[1], HEX);
     Serial.println(sgp.serialnumber[2], HEX);
     
     // If you have a baseline measurement from before you can assign it to start, to 'self-calibrate'
 mqtt.setServer(MQTT_SERVER, MQTT_PORT);
 //mqtt.setCallback(callback);
}
 int counter = 0;
void loop() {
  motion_detected = digitalRead(Vibrator);
     Serial.print("Vibrator: ");
     Serial.println(motion_detected);     
     delay(200);
  if (! sgp.IAQmeasure()) {
      Serial.println("Measurement failed");
      return;
      }
      
      Serial.print("TVOC "); Serial.print(sgp.TVOC); Serial.print(" ppb\t");
      Serial.print("eCO2 "); Serial.print(sgp.eCO2); Serial.println(" ppm");
      

      if (! sgp.IAQmeasureRaw()) {
        Serial.println("Raw Measurement failed");
        return;
      }
      
      Serial.print("Raw H2 "); Serial.print(sgp.rawH2); Serial.print(" \t");
      Serial.print("Raw Ethanol "); Serial.print(sgp.rawEthanol); Serial.println("");
 
      delay(1000);
      counter++;
      if (counter == 30) {
        counter = 0;

        uint16_t TVOC_base, eCO2_base;
        if (! sgp.getIAQBaseline(&eCO2_base, &TVOC_base)) {
          Serial.println("Failed to get baseline readings");
          return;
        }      
      } 
      int sensorvalue = digitalRead(SENSOR_OUTPUT_PIN);
      Serial.print("pir: ");
      Serial.println(sensorvalue);
      delay(500);
      
 if (mqtt.connect(MQTT_NAME, MQTT_USERNAME, MQTT_PASSWORD)) {
  sprintf(msg,"%d",motion_detected);
  //mqtt.publish("sensor/vibration",msg);
  sprintf(msg1,"%d",(int) sgp.TVOC);
  //mqtt.publish("sensor/tvoc",msg1);
  sprintf(msg2,"%d",(int) sgp.eCO2);
  //mqtt.publish("sensor/co2",msg2);
  sprintf(msg3,"%d",sensorvalue);
  //mqtt.publish("sensor/pir",msg3);
  s = String(msg);
  s = s+"/"+msg1+"/"+msg2+"/"+msg3;
  mqtt.publish("esp8266/sensors",s.c_str());
  Serial.println("connected with mqtt server");
 }
 else{
  Serial.println("not connected");
 }
 delay(10000);
}
