#include <usbhid.h>
#include <hiduniversal.h>
#include <usbhub.h>
#include "g502_rptparser.h"
#include <SPI.h>

USB                                             Usb;
USBHub                                          Hub(&Usb);
HIDUniversal                                    Hid(&Usb);
MouseEvents                                     MouseEvents;
G502ReportParser                                G502(&MouseEvents);

// Message head and tail - magical number found with USB sniffing
uint8_t dataHead[] = {0x11, 0xFF, 0x02, 0x3B};
uint8_t dataTail[10] = {0};

uint16_t colorIndex = 0;
uint32_t prevMillis = 0;

// LED enum
enum LED
{
  dpiLed,
  logoLed
};

// Function prototypes
void clearBuffers(void);
void setLedColor(LED led, uint8_t redVal, uint8_t greenVal, uint8_t blueVal);
void HSVRainbow(uint16_t angle, uint8_t * redVal, uint8_t * greenVal, uint8_t * blueVal);
void setMouseColors(void);


void setup()
{
  Serial.begin( 115200 );
  Serial.println("Start");

  if (Usb.Init() == -1)
      Serial.println("OSC did not start.");

  delay( 200 );

  if (!Hid.SetReportParser(0, &G502))
      ErrorMessage<uint8_t>(PSTR("SetReportParser"), 1  );
}

void loop()
{ 
  if(millis() - prevMillis >= 30){
    prevMillis = millis();
    setMouseColors();
  }
  Usb.Task();
}

void clearBuffers(void){
  //Interface-0: 8 Byte
  uint8_t buff0[8];
  memset(buff0, 0, sizeof(buff0));
  for(int i = 0; i < 10; i++)
    for(int j = 0; j < 5; j++)
      Usb.inTransfer(0x00, j, sizeof(buff0), buff0);

  //Interface-1: 20 Byte
  uint8_t buff1[20];
  memset(buff1, 0, sizeof(buff1));
  for(int i = 0; i < 10; i++)
    for(int j = 0; j < 5; j++)
      Usb.inTransfer(0x01, j, sizeof(buff1), buff1);
}

void setLedColor(LED led, uint8_t redVal, uint8_t greenVal, uint8_t blueVal){
  uint8_t data[20];
  memset(data, 0, sizeof(data));
  
  //Add Data Head: 0-3
  for(int i=0; i < sizeof(dataHead); i++)
    data[i] = dataHead[i];
  //Set Led: 4
  data[4] = led;
  //Set msg start: 5
  data[5] = 1;
  //Set red color: 6
  data[6] = redVal;
  //Set green color: 7
  data[7] = greenVal;
  //Set blue color: 8
  data[8] = blueVal;
  //Set msg end: 9
  data[9] = 2;
  //Add Data Tail: 10 - 19
  for(int i=(sizeof(data)-sizeof(dataTail)); i < sizeof(data); i++)
    data[i] = dataHead[i];

  Usb.ctrlReq(0x01, 0x00, 0x21, 0x09, 0x11, 0x02, 0x0001, sizeof(data), sizeof(data), data, NULL);
}

void HSVRainbow(uint16_t angle, uint8_t * redVal, uint8_t * greenVal, uint8_t * blueVal){
  float r = 0.0f, g = 0.0f, b = 0.0f;
  float a = angle;
  if(a <= 60.0f){
    r = 1.0f;
    g = a/60.0f;
    b = 0;
  }
  else if(60.0f < a && a <= 120.0f){
    r = (1.0f - ((a - 60.0f)/60.0f));
    g = 1.0f;
    b = 0.0f;
  }
  else if(120.0f < a && a <= 180.0f){
    r = 0.0f;
    g = 1.0f;
    b = (a - 120.0f)/60.0f;
  }
  else if(180.0f < a && a <= 240.0f){
    r = 0.0f;
    g = (1.0f - ((a - 180.0f)/60.0f));
    b = 1.0f;
  }
  else if(240.0f < a && a <= 300.0f){
    r = (a - 240.0f)/60.0f;
    g = 0.0f;
    b = 1.0f;
  }
  else if(300.0f < a && a <= 360.0f){
    r = 1.0f;
    g = 0.0f;
    b = (1.0f - ((a - 300.0f)/60.0f));
  }

  *redVal =  uint8_t(round(255.0f*r));
  *greenVal =  uint8_t(round(255.0f*g));
  *blueVal =  uint8_t(round(255.0f*b));
}

void setMouseColors(void){
  uint8_t *r, *g,*b;
  HSVRainbow(colorIndex,r,g,b);
  
  clearBuffers();
  setLedColor(dpiLed, *r, *g, *b);
  clearBuffers();
  setLedColor(logoLed, *r, *g, *b);
  
  colorIndex--;
  
  if(colorIndex > 360)
    colorIndex = 360;
}
