# main.py -- put your code here!
import pyb
from DHT22 import DHT22

# Turn blue LED on
blueled=pyb.LED(4)
blueled.on()

print("demarage du programe de test")

dht22 = DHT22("X1")

dht22.measure()

humidity = dht22.getHumidity()
temperature = dht22.getTemperature()

print("humidite : " + humidity)
print("temperature : " + temperature)