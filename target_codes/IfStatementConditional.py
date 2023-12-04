import machine
import utime

analogPin = 0
ledPin = 13
threshold = 400

adc_pin = machine.Pin(analogPin)
adc = machine.ADC(adc_pin)
p1 = machine.Pin(ledPin, machine.Pin.OUT)


while True:
    analogValue = adc.read_u16()
    if analogValue > threshold:
        p1.value(1)
    else:
        p1.value(0)
    print(analogValue)
    utime.sleep(2/1000)
