import machine
import utime

sensorPin = 0
baselineTemp = 20.0

adc_pin = machine.Pin(sensorPin)
adc = machine.ADC(adc_pin)

pins = []
for i in range(2, 5):
    pin = machine.Pin(i, machine.Pin.OUT)
    pin.value(0)
    pins.append(pin)

while True:
    sensorVal = adc.read_u16()
    print("Sensor Value: ", end="")
    print(sensorVal, end="")

    voltage = (sensorVal / 1024.0) * 5.0

    print(", Volts: ", end="")
    print(voltage, end="")

    print(", degree C: ", end="")
    temperature = (voltage - 0.5) * 100
    print(temperature)

    if (temperature < baselineTemp + 2):
        pins[0].value(0)
        pins[1].value(0)
        pins[2].value(0)
    elif temperature >= baselineTemp + 2 and temperature < baselineTemp + 4:
        pins[0].value(1)
        pins[1].value(0)
        pins[2].value(0)
    elif temperature >= baselineTemp + 4 and temperature < baselineTemp + 6:
        pins[0].value(1)
        pins[1].value(1)
        pins[2].value(0)
    elif temperature >= baselineTemp + 6:
        pins[0].value(1)
        pins[1].value(1)
        pins[2].value(1)
    utime.sleep(2/1000)