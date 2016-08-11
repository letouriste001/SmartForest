# main.py -- put your code here!
import pyb

import DHT22

# Turn blue LED on
blueled=pyb.LED(4)
blueled.on()

DHT22.init()
(hum, tem) = DHT22.measure()


while True:
    print("humidite : " + str(hum) + " temperature : " + (str(tem)))
    pyb.delay(3000)


