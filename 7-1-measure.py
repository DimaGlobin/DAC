import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# создаём переменные

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

# настраиваем обращение к GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)


# настройка подачу напряжения на тройку
def troyka_set(val):
    GPIO.output(troyka, val)

# настройка подачу напряжения на leds
def leds_set(val):
    GPIO.output(leds, val)

# перевод из десятичного числа в двоичное
def dec2bin(value):
    return [int(bit) for bit in bin(int(value))[2:].zfill(8)]

# перевод двоичного числа из листа в целое число
def bin2dec(list):
    weight = 128
    val = 0
    for i in range(0, 8):
        val += weight * list[i]
        weight /= 2
    
    return val
    
def adc_sar():
    list = [0] * 8
    for i in range(0, 8):
        list[i] = 1
        GPIO.output(dac, list)
        time.sleep(0.001)

        if(GPIO.input(comp) == 0):
            list[i] = 0

    return bin2dec(list)

data = []

try:
    print("Starting")
    start_time = time.time()
    

    GPIO.output(17, 1)
    
    # зарядка
    val = 0
    while(val <= 255 * 0.8):
        val = adc_sar()
        data.append(val)
        print("Voltage: {:.2f} V".format(val * 3.3 / 256))
        print(val)
        leds_set(dec2bin(val))
    
    charge_time = time.time() - start_time
    
    GPIO.output(17, 0)

   # разрядка
    val = 255
    while(val >= 255 * 0.05):
        val = adc_sar()
        data.append(val)
        print("Voltage: {:.2f} V".format(val * 3.3 / 256))
        leds_set(dec2bin(val))
    
    finish_time = time.time() - start_time
        
finally:
    print("Finishing")
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()

# обработка данных

plt.plot(data)
plt.show()

data_str = [str(item) for item in data]

with open("7-1_data.txt", "w") as outfile:
    outfile.write("\n".join(data_str))

with open("7-1_settings.txt", "w") as outfile:
    outfile.write("discret: {} s\nquant: {:.5f} V\n".format(finish_time / len(data), 3.3 / 256))
    outfile.write("charge time: {:.3f} s\nfinish time: {:.3f} s\n".format(charge_time, finish_time))

print("discret: {} s\n quant: {:.5f} V\n charge time : {:.3f} s\n".format(finish_time / len(data), 3.3 / 256, charge_time))