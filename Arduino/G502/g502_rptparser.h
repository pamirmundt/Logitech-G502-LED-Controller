#if !defined(__G502PTPARSER_H__)
#define __G502PTPARSER_H__

#include <usbhid.h>

struct MouseEventData
{
  uint8_t data1;
  uint8_t data2;
  uint8_t data3;
  uint8_t data4;
  uint8_t data5;
  uint8_t data6;
  uint8_t data7;
  uint8_t data8;
};


class MouseEvents
{
public:

	MouseEvents();

	virtual void OnMouseChanged(const MouseEventData *evt);
};

#define RPT_MOUSE_LEN	sizeof(MouseEventData)/sizeof(uint8_t)

class G502ReportParser : public HIDReportParser
{
	MouseEvents		*mouseEvents;

  uint8_t oldMouse[RPT_MOUSE_LEN];

public:
	G502ReportParser(MouseEvents *evt);

	virtual void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf);
};


#endif // __G502PTPARSER_H__
