import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac =[26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setup(dac, GPIO.OUT)

def d2b(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

try:
    t = float(input())
    while(True):
        value = 0
        while(True):
            if (value >= 256): break
            GPIO.output(dac, d2b(int(value)))
            time.sleep(t)
            value += 1
        
        value = 255

        while(True):
            if (value < 0): break
            GPIO.output(dac, d2b(int(value)))
            time.sleep(t)
            value -= 1

finally: 
    GPIO.output(dac, 0)
    GPIO.cleanup()

