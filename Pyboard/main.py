# main.py -- put your code here!
import pyb
#from AM2302 import AM2302
#from DHTSeries import DHTSeries as AM2302
import DHTSeries as DHT22
# Turn blue LED on
blueled=pyb.LED(4)
blueled.on()

print("demarage du programe de test")

# am2302 = AM2302()
#
# while True:
#     (hum, tem) = am2302.measure()
#     print("humidité : " + str(hum) + " temperature : " + str(tem))

DHT22.init()
pyb.delay(3000)

while True:
    (hum, tem) = DHT22.measure()
    print("humidité : " + str(hum) + " temperature : " + str(tem))
    pyb.delay(3000)
