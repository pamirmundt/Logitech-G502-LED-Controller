/* Parser for standard HID scale (usage page 0x8d) data input report (ID 3) */ 
#ifdef ARDUINO_SAM_DUE
#include <avr/dtostrf.h>
#endif
#include "g502_rptparser.h"

G502ReportParser::G502ReportParser(MouseEvents *evt) :
	mouseEvents(evt)
{}

void G502ReportParser::Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf)
{
	bool match = true;

	// Checking if there are changes in report since the method was last called
	for (uint8_t i=0; i<RPT_MOUSE_LEN; i++) {
		if( buf[i] != oldMouse[i] ) {
			match = false;
			break;
		}
  }
  	// Calling Game Pad event handler
	if (!match && mouseEvents) {
    mouseEvents->OnMouseChanged((const MouseEventData*)buf);

		for (uint8_t i=0; i<RPT_MOUSE_LEN; i++) oldMouse[i] = buf[i];
	}
}

MouseEvents::MouseEvents(){}

void MouseEvents::OnMouseChanged(const MouseEventData *evt)
{
  /*
  Serial.print(evt->data1);
  Serial.print(" ");
  Serial.print(evt->data2);
  Serial.print(" ");
  Serial.print(evt->data3);
  Serial.print(" ");
  Serial.print(evt->data4);
  Serial.print(" ");
  Serial.print(evt->data5);
  Serial.print(" ");
  Serial.print(evt->data6);
  Serial.print(" ");
  Serial.print(evt->data7);
  Serial.print(" ");
  Serial.println(evt->data8);
  */
}
