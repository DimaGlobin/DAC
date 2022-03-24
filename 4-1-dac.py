import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

dac =[26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setup(dac, GPIO.OUT)

def d2b(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

try: 
    while (True):
        print("Put the number from 0 to 255: ")
        value = input()
        if (value == "q"): 
            break

        if (value.isdigit() == False): 
            print("The number is not integer")
            break
        
        if (float(value) - float(value)//1 != 0.0):
            print("The number type is double")
            break
        
        if (int(value) > 255 or int(value) < 0):
            print("Value is not for 8 bit(")
            break

        GPIO.output(dac, d2b(int(value)))
        print("Voltage is: ", format(int(value)*3.3/256), "\n")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    

