import pyb
from pyb import Pin
from pyb import ExtInt

# We need to use global properties here as any allocation of a memory (aka declaration of a variable)
# during the read cycle causes non-acceptable delay and we are loosing data than
data = None
timer = None
micros = None
dhttype = 0  # 0=DHT11 1=DHT21/DHT22

DATASIZE = 42  # we have 42 falling edges during data receive

times = list(range(DATASIZE))
index = 0


# The interrupt handler
def _interuptHandler(line):
    global index
    global times
    global micros
    # print("edge callback")
    times[index] = micros.counter()
    if index < (DATASIZE - 1):  # Avoid overflow of the buffer in case of any noise on the line
        index += 1


def init(timer_id=2, data_pin='Y2', the_dhttype='DHT22'):
    global data
    global micros
    global timer
    global dhttype
    
    if (the_dhttype == 'DHT11'):
        dhttype = 0
    else:
        dhttype = 1
    # Configure the pid for data communication
    data = Pin(data_pin)
    # Save the ID of the timer we are going to use
    timer = timer_id
    # setup the 1uS timer
    micros = pyb.Timer(timer, prescaler=83, period=0x3fffffff)  # 1MHz ~ 1uS
    # Prepare interrupt handler
    ExtInt(data, ExtInt.IRQ_FALLING, Pin.PULL_UP, None)
    ExtInt(data, ExtInt.IRQ_FALLING, Pin.PULL_UP, _interuptHandler)
    data.high()
    pyb.delay(250)


# Start signal
def _do_measurement():
    global data
    global micros
    global index
    # Send the START signal
    data.init(Pin.OUT_PP)
    data.low()
    micros.counter(0)
    while micros.counter() < 20000:
        pass
    data.high()
    micros.counter(0)
    while micros.counter() < 30:
        pass
    # Activate reading on the data pin
    index = 0
    data.init(Pin.IN, Pin.PULL_UP)
    # Till 5mS the measurement must be over
    pyb.delay(10)


# Parse the data read from the sensor
def _process_data():
    global dhttype
    global times
    
    i = 2  # We ignore the first two falling edges as it is a respomse on the start signal
    result_i = 0
    result = list([0, 0, 0, 0, 0])
    while i < DATASIZE:
        result[result_i] <<= 1
        if times[i] - times[i - 1] > 100:
            result[result_i] += 1
        if (i % 8) == 1:
            result_i += 1
        i += 1
    [int_rh, dec_rh, int_t, dec_t, csum] = result
    
    if dhttype == 0:  # dht11
        humidity = int_rh  # dht11 20% ~ 90%
        temperature = int_t  # dht11 0..50°C
    else:  # dht21,dht22
        humidity = ((int_rh * 256) + dec_rh) / 10
        temperature = (((int_t & 0x7F) * 256) + dec_t) / 10
        if (int_t & 0x80) > 0:
            temperature *= -1
    
    comp_sum = int_rh + dec_rh + int_t + dec_t
    if (comp_sum & 0xFF) != csum:
        raise ValueError('Checksum does not match')
    return (humidity, temperature)


def measure():
    _do_measurement()
    if index != (DATASIZE - 1):
        raise ValueError('Data transfer failed: %s falling edges only' % str(index))
    return _process_data()
    
    # using:
    # import DHT22
    # DHT22.init()
    # DHT22.measure()