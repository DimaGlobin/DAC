import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac =[26, 19, 13, 6, 5, 11, 9, 10]

comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def d2b(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = d2b(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    for value in range(256):
        signal = num2dac(value)
        voltage = value * 3.3 / 256
        time.sleep(0.0007)
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 0:
            print("Value is: {:3}, volatge = {:.2f}".format(value, voltage))
            return

try:
    while True:
        adc()


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    
