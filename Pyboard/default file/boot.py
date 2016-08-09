# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import pyb
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse

# REPL over UART
REPL=pyb.UART(1,115200)
pyb.repl_uart(REPL)

blueled=pyb.LED(4)
blueled.on()

#import pyb
##import os
#from ds3231 import DS3231
#
## REPL over UART
#REPL=pyb.UART(3,115200)
#pyb.repl_uart(REPL)
##os.dupterm(REPL)
#
## USB Mode
#pyb.usb_mode(None)       # Kill serial device
##pyb.usb_mode('CDC')      # Act as a serial device
##pyb.usb_mode('CDC+MSC')  # Act as a serial device and a storage device
##pyb.usb_mode('CDC+HID')  # Act as a serial device and a mouse ** SDCARD **
#
#print('')
#print('********************************')
#print('PYBOARD MICROCONTROLLER')
#print('********************************')
#print('RTC PYBOARD')
#rtc1=pyb.RTC()
#print(rtc1.datetime())
#print('********************************')
#print('RTC DS3231')
#rtc2=DS3231()
#print(rtc2.get_time())
#print('********************************')
#print('')
#
## Main script to run after this one
pyb.main('mainTest.py')
#pyb.main('test.py')
#pyb.main('none.py')
