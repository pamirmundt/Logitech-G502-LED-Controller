import usb.core
import usb.util
import sys
import datetime, time

# Logitech G502 Proteus Spectrum Mouse
# ReadEvent (left/right clicks, wheel, other buttons and etc.)
# Set Color for logo and DPI

# This demo displays HSV rainbow colors on DPI and Logo LEDs

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

    getMouseEvent()

    try:
        #Send configure for dpi color
        ret = k_dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0211, wIndex=0x0001, data_or_wLength=data)
    except:
        pass

    getMouseEvent()


    try:
        #Read return report
        data = k_dev.read(kEndpointAddress, ret)
    except:
        pass

def logoColor(R,G,B):
    color = [R,G,B]

    data = start + [1] + [1] + color + [2] + end

    getMouseEvent()

    try:
        #Send configura for logo color
        ret = k_dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0211, wIndex=0x0001, data_or_wLength=data)
    except:
        pass

    getMouseEvent()

    try:
        #Read return report
        data = k_dev.read(kEndpointAddress, ret)
    except:
        pass

def HSVRainbow(angle=0.0):
    R = G = B = 0.0

    if(angle <= 60.0):
        R = 1.0
        G = (angle/60.0)
        B = 0.0
    elif(60 < angle <= 120):
        R = (1.0 - ((angle - 60.0)/60.0))
        G = 1.0
        B = 0.0
    elif(120 < angle <= 180):
        R = 0.0
        G = 1.0
        B = (angle - 120.0)/60.0
    elif(180 < angle <= 240):
        R = 0.0
        G = (1.0 - ((angle - 180.0)/60.0))
        B = 1.0
    elif(240 < angle <= 300):
        R = (angle - 240.0)/60.0
        G = 0.0
        B = 1.0
    elif(300 < angle <= 360):
        R = 1.0
        G = 0.0
        B = (1.0 - ((angle - 300.0)/60.0))

    return [R,G,B]

def displayRainbow():
    for i in range (360,0,-1):
        R = int(HSVRainbow(i)[0] * 255.0)
        G = int(HSVRainbow(i)[1] * 255.0)
        B = int(HSVRainbow(i)[2] * 255.0)

        logoColor(R,G,B)
        dpiColor(R,G,B)
        print(i)


def runForever():
    global colorIndex
    global interval
    global endTime
    global startTime

    colorIndex %= 360


    #*** Rainbow ***
    R = int(HSVRainbow(colorIndex)[0] * 255.0)
    G = int(HSVRainbow(colorIndex)[1] * 255.0)
    B = int(HSVRainbow(colorIndex)[2] * 255.0)

    #Update Mouse LEDs
    logoColor(R,G,B)
    dpiColor(R,G,B)

    #Update Environment LEDs
    pi.set_PWM_dutycycle(rPin, R)
    pi.set_PWM_dutycycle(gPin, G)
    pi.set_PWM_dutycycle(bPin, B)

    #Reverse
    colorIndex += 2

    #***************

    endTime = time.time()

    delta = interval - (endTime - startTime)

    if delta >= 0:
        time.sleep(delta)

    startTime = time.time()


use_usb()

#PiGPIO
pi = pigpio.pi()
if not pi.connected:
   exit()

rPin = 17 #GPIO 17
gPin = 27 #GPIO 27
bPin = 22 #GPIO 22

pi.set_PWM_frequency(rPin, 200)
pi.set_PWM_frequency(gPin, 200)
pi.set_PWM_frequency(bPin, 200)

#Thread variables
interval = 2.0*(12.0/360.0) #Second - Total color rainbow takes 12 second in the original demo / 360 colors in the pallete / color interval: 2
colorIndex = 0
startTime = 0
endTime = 0


try:
    startTime = time.time()
    while True:
        runForever()
except KeyboardInterrupt:
    pass



stop_usb()
pi.stop()
