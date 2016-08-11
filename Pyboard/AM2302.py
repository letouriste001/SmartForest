#########

import pyb
from pyb import Pin
from pyb import ExtInt

_micro = None
_time = []
_indexPulse = 0

class AM2302:
    """
    Classe de gestion du capteur AM2302
    
    """
    def __init__(self, pinName="Y1"):
    
        #self._indexPulse = 0  # suivi des impulsions de comunication
        #self._time = []  # liste les temp de reception des données
        self._data = []  # liste des bits reçus
        self._humidity = 0.0  # humidité mesurée par le capteur
        self._temperature = 0.0  # temperature mesurée par le capteur
        self._pin = pyb.Pin(pinName)  # pin ou est branché le capteur
        
        global _micro
        _micro = pyb.Timer(2, prescaler=83, period=0x3fffffff)  # definition de la pin
        #self._micro = pyb.Timer(2, prescaler=83, period=0x3fffffff)  # Timer 2 initialiser a 1µs (1MHz)
        #self._event = None
    
        pyb.ExtInt(self._pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)
        pyb.ExtInt(self._pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self._callback)
        #self._event = ExtInt(self._pin, ExtInt.IRQ_FALLING, Pin.PULL_UP, self._callback)
        pyb.delay(5000)  # delais d'initialisation du capteur
        self._pin.init(Pin.OUT_PP)  # configuration de la pin en emission
        self._pin.high()  # Mise de la pin a 1
        pyb.delay(250)
    
    
    def getHumidity(self):
        """
        retourne la valeur d'humidité mesurée par le capteur
        
        :return: la mesure d'humiditée
        :rtype: float
        """
        return self.humidity
    
    def getTemperature(self):
        """
                retourne la valeur de temperature mesurée par le capteur

                :return: la mesure d'humiditée
                :rtype: float
                """
        return self.temperature
    
    def _callback(self,line):
        """
        Fonction de callback qui ajoute la valeur de compteur dans la liste de temps
        :param line:
        """
        global _indexPulse
        global _time
        global _micro
        self.debug.off()
        _time[_indexPulse] = _micro.counter()
        self._indexPulse += 1
    
    def _initMeasure(self):
        """
        Fonction pour initialiser la mesure
        """
        
        global _micro
        global _indexPulse
        # Sequence pour initialiser la lecture du capteur
        self._pin.low()
        _micro.counter(0)
        while(_micro.counter() < 20000):
            pass
        self._pin.high()
        _micro.counter(0)
        while (_micro.counter() < 40):
            pass
        
        _indexPulse = 0  # mise a zero de l'index
        self._pin.init(Pin.IN, Pin.PULL_UP)  # configuration de la pin en reception
    
    def _convertTimeToBit(self):
        """
        Fonction qui convertie les temp de comunication en bit de donnée
        """
        global _time
        i = 2
        print("taille du tableau : " + str(len(self._time)))
        while(i < 41):
            print("index : " + str(i))
            if(_time[i] < 100):
                self._data.append("0")
            else:
                self._data.append("1")
            i += 1
    
    def measure(self):
        """
        fonction qui recupere la valeur d'humidité et de temperatude du capteur
        :return: humidité et temperature
        """
        self._initMeasure()
        pyb.delay(1000)
        
        self._convertTimeToBit()
        
        hh = self._byteDataToString(start=0)  # octet high humidity
        lh = self._byteDataToString(start=8)  # octet low humidity
        ht = self._byteDataToString(start=16)  # octet high temperature
        lt = self._byteDataToString(start=24)  # octet low temperature
        pb = self._byteDataToString(start=32)  # octet parity bit
        
        self._checkSum(hh, lh, ht, lt, pb)
        
        self.humidity = int((hh + lh), 2) / 10
        self.temperature = int((ht + lt), 2) / 10
        
        return (self.humidity, self.measure())
    
    def _byteDataToString(self, start=0, nbBits=7):
        """
        :param start: index du debut de l'octet de donnée dans le tableau
        :param nbBits: nombre de bit a prendre pour recuperer un ou plusieur octets
        :return: une chaine de caractere qui contien un ou plusieur octets de données
        """
        tmp = ""
        
        for i in range(start, start + nbBits ):
            tmp = tmp + self._data[i]
        return tmp
    
    def _checkSum(self, hh, lh, ht, lt, pb):
        """
        fonction qui verifie la parité des donées
        :param hh: octet high humidity
        :param lh: octet low humidity
        :param ht: octet high temperature
        :param lt: octet low temperature
        :param pb: octet parity bit
        """
        checkSum = int(str(pb), 2)
        calcCheckSum = int(hh, 2) + int(lh, 2) + int(ht, 2) + int(lt, 2)
        if (calcCheckSum != checkSum):
            raise ValueError("Bad checksum, Bad communication with sensor")
    
