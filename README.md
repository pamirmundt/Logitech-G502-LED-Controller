# Logitech G502 Mouse with Python
A dirty code where you can set Logitech G502 mouse led color and read click/position events with Python. The USB packages send from the PC driver and mouse sniffed with USBlyzer on a Windows machine. Attached demo codes tested only on a Raspberry Pi 3 (Raspbian).

There are two interfaces under mouse:

#### Interface 0: Mouse Device
 - Get interrupt events (cursor move, click, wheel and etc.)

#### Interface 1: Keyboard Device (I guess)
 - Set RGB LED colors (Logo LED and DPI LED)

### Notes:
- Interrupt events should be read (Interface-0) continuously. Otherwise mouse buffer fills and you cannot send any more data to Interface-1.
