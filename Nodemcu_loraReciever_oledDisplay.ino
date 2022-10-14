#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define i2c_Address 0x3c //initialize with the I2C addr 0x3C Typically eBay OLED's
//#define i2c_Address 0x3d

char data[50];
//Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SH1106G display =   Adafruit_SH1106G(128, 64, &Wire, -1);


void setup() 
{
  Serial.begin(9600);
  Serial.println("LoRa Receiver");
  if (!LoRa.begin(433E6)) 
  {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  delay(250); // wait for the OLED to power up
  display.begin(i2c_Address, true); // Address 0x3C default
 //display.setContrast (0); // dim display
  display.display();
  delay(2000);
  display.clearDisplay();
}
void loop() 
{
  // To store the received message in a string, uncomment line 16 and 24.
   //String str="";
  int packetSize = LoRa.parsePacket();
  if (packetSize) 
  {
    Serial.print("Received packet '");
    while (LoRa.available()) 
    {
      Serial.print((char)LoRa.read());
      //str=str+((char)LoRa.read());
//    display.print((char)LoRa.read());   
    }
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());
    display.setTextSize(1);
    display.setTextColor(SH110X_WHITE);
    display.setCursor(0, 0);
   // display.println(str);
    display.display();
  }
}
