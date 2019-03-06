import usb.core
import usb.util
import sys

# Logitech G502 Proteus Spectrum Mouse
# ReadEvent (left/right clicks, wheel, other buttons and etc.)
# Set Color for logo and DPI

# This demo sets the color of DPI and Logo LEDs

#Mouse Interface
#Interface: 0
mEndpointAddress = 0x81

#Keyboard Interface
#Interface: 1
kEndpointAddress = 0x82

#Magic number, found on usb sniffing
start = [0x11, 0xFF, 0x02, 0x3B]

end = [0x00]*10

def use_usb():
    global k_dev
    global m_dev
    k_dev = usb.core.find(idVendor=0x046d, idProduct=0xc332)

    if k_dev is None:
        raise ValueError('Device not found')

    #-------------------------------------
    #
    #   Mouse Device - Interface 0
    #
    #-------------------------------------

    m_dev = k_dev

    try:
        m_dev.detach_kernel_driver(0)
    except:
        print("No mouse device to detach")
    finally:
        #Attach and detach again
        m_dev.attach_kernel_driver(0)
        m_dev.detach_kernel_driver(0)

    usb.util.claim_interface(m_dev,0)

    m_dev.set_interface_altsetting(interface=0,alternate_setting=0)

    #-------------------------------------
    #
    #   Keyboard Device - Interface 1
    #
    #-------------------------------------

    try:
        k_dev.detach_kernel_driver(1)
    except:
        print("No keyboard device to detach")
    finally:
        #Attach and detach again
        k_dev.attach_kernel_driver(1)
        k_dev.detach_kernel_driver(1)

    usb.util.claim_interface(k_dev,1)

    k_dev.set_interface_altsetting(interface=1,alternate_setting=0)

def getMouseEvent():
    try:
        # Read 8 bytes of data
        return( m_dev.read(0x81, 8, 1) )

    except:
        pass
        #print("nothing to read")
    finally:
        pass

    return None


def stop_usb():
    #Stop Mouse
    usb.util.release_interface(m_dev,0)
    m_dev.attach_kernel_driver(0)

    #Stop Keyboard
    usb.util.release_interface(k_dev,1)
    k_dev.attach_kernel_driver(1)

def dpiColor(R,G,B):
    color = [R,G,B]

    data = start + [0] + [1] + color + [2] + end

    ret = 0

    try:
        #Send configure for dpi color
        ret = k_dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0211, wIndex=0x0001, data_or_wLength=data)
    except:
        pass

    try:
        #Read return report - mouse is sending back a report after color set
        data = k_dev.read(kEndpointAddress, ret)
    except:
        pass

def logoColor(R,G,B):
    color = [R,G,B]

    data = start + [1] + [1] + color + [2] + end

    try:
        #Send configura for logo color
        ret = k_dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0211, wIndex=0x0001, data_or_wLength=data)
    except:
        pass

    try:
        #Read return report - mouse is sending back a report after color set
        data = k_dev.read(kEndpointAddress, ret)
    except:
        pass




# Start using USB
use_usb()

# Change logo LED
logoColor(255,0,0) #RED

# Change DPI LED
dpiColor(255,0,0) #RED


# Stop using USB
stop_usb()