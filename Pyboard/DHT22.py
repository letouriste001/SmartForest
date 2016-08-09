#########

import pyb


class DHT22:
    def __init__(self, pinName):
        self.data = []
        self.humidity = None
        self.temperature = None
        self.pinName = pinName
        self.pin = pyb.Pin(self.pinName, pyb.Pin.OUT_PP)
        self.pin.high()
    
    def getHumidity(self):
        return self.humidity
    
    def getTemperature(self):
        return self.temperature
    
    def _detectBit(self):
        cpt = 0
        while(i <= 80):
            if (self.pin.value() != 1 and i == 25 or i == 27 or i == 28):
                return 0
            elif(self.pin.value() != 1 and i == 69 or i == 70 or i == 71):
                return 1
            elif(self.pin.value() != 1 and i > 75):
                return -1
            pyb.udelay(1)
            cpt += 1
    
    def _transmit(self, delay, level, sequence):
        cpt = 0
        while (cpt <= delay):
            if (self.pin.value() < level):
                raise ValueError("transmit error" + sequence)
            pyb.udelay(1)
    
    def _initMeasure(self):
        self.pin = pyb.Pin(self.pinName, pyb.Pin.OUT_PP)
        self.pin.low()
        pyb.delay(10)
        self.pin.high()
        pyb.udelay(35)
        self.pin = pyb.Pin(self.pinName, pyb.Pin.IN, pull=pyb.Pin.PULL_NONE)
    
    def measure(self):
        
        negativeTemp = False
        self._initMeasure()
        self._transmit(delay=80, level=0, sequence="sensor signal pull low")
        self._transmit(delay=80, level=1, sequence="sensor signal pull high")
        for i in range(0, 39):
            tmp = self._detectBit
            if (tmp == -1):
                raise ValueError("Bad communication with sensor")
            else:
                self.data.append(tmp)
        if (self._checkSum() == 1):
            self.humidity = self._convertBit(start=0, range=15)
            if (self.data[16] == 1):
                negativeTemp = True
                self.data[16] = 0
            self.temperature = self._convertBit(start=16, range=15)
            if (negativeTemp):
                self.temperature = self.temperature * -1
    
    def _convertBit(self, start, range):
        tmp = self._byteDataToString(start=start, range=range)
        value = int(tmp, 2) / 10
        return value
    
    def _byteDataToString(self, start, range=7):
        for i in start(start, start + range):
            tmp = tmp + self.data[i]
        return tmp
    
    def _checkSum(self):
        a = self._byteDataToString(start=0)
        b = self._byteDataToString(start=8)
        c = self._byteDataToString(start=16)
        d = self._byteDataToString(start=24)
        checkSum = int(self._byteDataToString(start=32), 2)
        calcCheckSum = int(a, 2) + int(b, 2) + int(c, 2) + int(d, 2)
        if (calcCheckSum != checkSum):
            raise ValueError("Bad checksum, Bad communication with sensor")
        else:
            return 1
