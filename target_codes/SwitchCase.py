import machine
import utime

analogPin = 0
sensorMin = 0
sensorMax = 600

new_min = 0
new_max = 3

adc_pin = machine.Pin(analogPin)
adc = machine.ADC(adc_pin)

while True:
    sensorReading = adc.read_u16()
    local_range = int((sensorReading - sensorMin) * (new_max - new_min) / (sensorMax - sensorMin) + new_min)

    if local_range == 0:
        print("dark")
    elif local_range == 1:
        print("dim")
    elif local_range == 2:
        print("medium")
    elif local_range == 3:
        print("bright")
    
    utime.sleep(2)
