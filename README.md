# Logitech G502 Mouse with Python
A dirty code where you can set Logitech G502 mouse led color and read click/position events with Python. The USB packages send from the PC driver and mouse sniffed with USBlyzer software on a Windows machine. Attached demo codes tested only on a Raspberry Pi 3 (Raspbian). Sniffed files can be found under the USBlyzer folder. `interrupt.ulz` file has interrupt packages and `firstPlug.ulz` file has first time USB plug packages.

There are two interfaces under mouse:

#### Interface 0: Mouse Device
 - Get interrupt events (cursor move, click, wheel and etc.)

#### Interface 1: Keyboard Device (I guess)
 - Set RGB LED colors (Logo LED and DPI LED)

### Notes:
- Interrupt events should be read (Interface-0) continuously. Otherwise mouse buffer fills and you cannot send any more data to Interface-1.

## Board and Schematics
The system consists of 3 different boards: (1) Arduino UNO, (2)USB Host Shield 2.0 and (3)a custom LED controller/power supply board.

|     Layer     | Board Name                          | Board Description                   |
| ------------- | ----------------------------------- | ----------------------------------- |
|  1(bottom)    | Arduino UNO                         | MCU                                 |
|  2(middle)    | USB Host Shield 2.0                 | USB Controller in Host Mode         |
|  3(top)       | LED Controller and Power Supply (*) | RGB Led controller and 5V regulator |

(*) Eagle CAD files (.brd, .sch) can be found in the repo

## Future Improvements
- [ ] Switching regulator for 5V
- [ ] Single board layout
- [ ] Inconsistent color transitions between LED strip and G502 LEDs
