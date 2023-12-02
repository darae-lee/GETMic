import machine
# import utime
machine.load_board(__file__)
analogPin = 0
ledPin = 13
threshold = 400
interactor = machine.UserInteract()
codes = interactor.codes


adc_pin = machine.Pin(analogPin)
adc = machine.ADC(adc_pin)
p1 = machine.Pin(ledPin, machine.Pin.OUT)


for inter in [100, 300, 500]:
    interactor.interact(inter)
    analogValue = adc.read_u16()
    if analogValue > threshold:
        print("on")
        p1.value(1)
    else:
        print("off")
        p1.value(0)
    print(analogValue)
    # utime.sleep(2)