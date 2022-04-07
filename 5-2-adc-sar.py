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

def adc1():
    value = 128
    values = [128, 64, 32, 16, 8, 4, 2, 1]

    list1 = [[], [], [], [], [], [], [], [], []]

    for i in range(9):
        for j in range(8):
            list1[i].append(0)

    counterstr = 0
    countersto = 0

    for i in range(8):
        list1[i] = d2b(values[i])

    while(countersto < 8 and counterstr < 9):
        signal = num2dac(value)
        time.sleep(0.0007)
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 1:
           for i in range(counterstr + 1, len(list1)):
              list1[i][countersto] = 1
        else:
            for i in range(counterstr + 1, len(list1)):
              list1[i][countersto] = 0
        value //= 2
        counterstr += 1
        countersto += 1

    result = 0

    for j in range(8):
        result += list1[8][j] * 2 ** (8 - j - 1)

    voltage = result * 3.3 / 256

    print("Value is: {:3}, volatge = {:.2f}".format(result, voltage))
    return

try:
    while True:
       adc1()
    #adc1()

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    
