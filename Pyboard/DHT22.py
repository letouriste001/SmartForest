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
        #print(" debug fonction _detectBit")
        cpt = 0
        while(cpt <= 80):
            #print(" debug fonction _detectBit while")
            if (self.pin.value() != 1 and cpt == 25 or cpt == 27 or cpt == 28):
                return 0
            elif(self.pin.value() != 1 and cpt == 69 or cpt == 70 or cpt == 71):
                return 1
            elif(self.pin.value() != 1 and cpt > 75):
                return -1
            pyb.udelay(1)
            cpt += 1
    
    def _transmit(self, level, sequence):
        #print(" debug fonction _transmit")
        cpt = 0
        while (cpt <= 80):
            #print(" debug fonction _transmit while")
            if (self.pin.value() < level):
                raise ValueError("transmit error" + sequence)
            pyb.udelay(1)
            cpt += 1
    
    def _initMeasure(self):
        #print(" debug fonction _initMeasure")
        self.pin = pyb.Pin(self.pinName, pyb.Pin.OUT_PP)
        self.pin.low()
        pyb.delay(10)
        self.pin.high()
        pyb.udelay(35)
        self.pin = pyb.Pin(self.pinName, pyb.Pin.IN, pull=pyb.Pin.PULL_NONE)
    
    def measure(self):
        #print(" debug fonction measure")
        negativeTemp = False
        self._initMeasure()
        self._transmit(level=0, sequence="sensor signal pull low")
        self._transmit(level=1, sequence="sensor signal pull high")
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

        self.pin = pyb.Pin(self.pinName, pyb.Pin.OUT_PP)
        self.pin.high()
    
    def _convertBit(self, start, range):
        print(" debug fonction _convertBit")
        tmp = self._byteDataToString(start=start, range=range)
        value = int(tmp, 2) / 10
        return value
    
    def _byteDataToString(self, start, range=7):
        print(" debug fonction _byteDataToString")
        tmp = None
        for i in range(start, start + range):
            ########## TODO debug
            #Traceback (most recent call last):
            #   File "main.py", line 13, in <module>
            #   File "DHT22.py", line 66, in measure
            #   File "DHT22.py", line 93, in _checkSum
            #   File "DHT22.py", line 88, in _byteDataToString
            # TypeError: unsupported types for __add__: 'NoneType', 'bound_method'
            tmp = tmp + self.data[i]
        return tmp
    
    def _checkSum(self):
        print(" debug fonction _checkSum")
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
