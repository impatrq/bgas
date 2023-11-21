import pyRTOS
from machine import ADC, Pin, I2C, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import onewire, ds18x20
import utime
from MQ2 import MQ2

button_on_pin = Pin(27, Pin.IN)
button_slide_pin = Pin(26, Pin.IN)
button_time_pin = Pin(25, Pin.IN)
on = 0
slide = 0
button_on = 0
button_slide = 0
birth = 0
tiempo_diasU = 0
tiempo_diasV = 0

# Configurar el pin del sensor de presión MPX5999D
pin_adc = Pin(14)
adc = ADC(pin_adc)
adc.atten(ADC.ATTN_11DB)
max_pressure = 1000.0  # Presión máxima en kPa
adc_resolution = 4096  # Resolución del ADC

#config para MQ2 YEAHHH
pin = Pin(4)
sensor = MQ2(pinData = pin, baseVoltage = 5)

# I2C LCD Configuration
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# DS18X20 Temperature Sensor Configuration
ds_pin = Pin(15)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print(roms)

#calibrar MQ2
#sensor.calibrate()
#print("Base resistance:{0}".format(sensor._ro))

def task_on(self):
    while True:
        global on
        global button_on
        if button_on == 1:
            if on == 0:
                on = 1
                button_on = 0
            else:
                on = 0
                button_on = 0
        yield [pyRTOS.timeout(0.001)]

def task_slide(self):
    while True:
        global button_slide
        global slide
        global on
        global tiempo_diasU, tiempo_diasV
        global sensor

        if slide == 0 and on == 1:
            adc_value = adc.read()
            adc_value1 = adc_value - 58
            pressure = (adc_value1 / adc_resolution) * max_pressure
            lcd.move_to(0, 0)
            lcd.putstr("Presion:")
            lcd.move_to(0, 1)
            lcd.putstr("{:.2f} kPa".format(pressure))
            print(pressure)
                
            if button_slide == 1:
                slide = 1
                button_slide = 0
                lcd.clear()
                utime.sleep(1)


        elif slide == 1 and on == 1:
            try:
                ds_sensor.convert_temp()
                temperature = ds_sensor.read_temp(roms[0])
                lcd.move_to(0, 0)
                lcd.putstr("Temperatura:")
                lcd.move_to(0, 1)
                lcd.putstr("{:.2f} C".format(temperature))
                print(temperatura)
            except:
                lcd.move_to(0, 0)
                lcd.putstr("Temperatura:")
                lcd.move_to(0, 1)
                lcd.putstr("no disponible")
            
            if button_slide == 1:
                slide = 2
                button_slide = 0
                lcd.clear()
                utime.sleep(1)

        elif slide == 2 and on == 1:
            if birth > 0:
                global tiempo_diasU
                if tiempo_diasU > 0:
                    lcd.move_to(0, 0)
                    lcd.putstr("Eficiente en:")
                    lcd.move_to(0, 1)
                    lcd.putstr(f"{tiempo_diasU} dias")
                elif tiempo_diasV > 0:
                    lcd.move_to(0, 0)
                    lcd.putstr("Eficiente, vence")
                    lcd.move_to(0, 1)
                    lcd.putstr(f"en: {tiempo_diasV} dias")
                else:
                    print(tiempo_diasU, tiempo_diasV)
                    lcd.move_to(0, 0)
                    lcd.putstr("Gen. iniciado")
                    lcd.move_to(0, 1)
                    lcd.putstr(f"hace: {tiempo_diasU} dias")
            else:
                lcd.move_to(0, 0)
                lcd.putstr("Generador no")
                lcd.move_to(0, 1)
                lcd.putstr("iniciado")
                
            if button_slide == 1:
                slide = 0
                button_slide = 0
                lcd.clear()
                utime.sleep(1)
        else:
            lcd.clear()
            """
        elif slide == 2 and on == 1:
            try:
                lcd.move_to(0, 0)
                lcd.putstr("Metano:")
                lcd.move_to(0, 1)
                metano = sensor.readSmoke()
                lcd.putstr("{:.2f} ppm".format(metano))
            except:
                lcd.move_to(0, 0)
                lcd.putstr("Metano:")
                lcd.move_to(0, 1)
                lcd.putstr("no disponible")
            
            if button_slide == 1:
                slide = 3
                button_slide = 0
                utime.sleep(1)
"""
        yield [pyRTOS.timeout(0.1)]

def task_button_on(self):
    while True:
        global button_on, button_on_pin
        if button_on_pin.value() == True:
            button_on = 1
            lcd.clear()
            utime.sleep(1)
        yield [pyRTOS.timeout(0.01)]


def task_button_slide(self):
    while True:
        global button_slide
        if button_slide_pin.value() == True:
            button_slide = 1
        yield [pyRTOS.timeout(0.01)]

def task_button_time(self):
    while True:
        global birth
        if button_time_pin.value() == True:
            birth = utime.time()
        yield [pyRTOS.timeout(0.01)]

def task_time(self):
    while True:
        global birth
        global tiempo_diasU
        global tiempo_diasV
        if birth == True:
            tiempo_actual = utime.time()
            
            tiempo_transcurrido = tiempo_actual - birth
            tiempo_sec = int(tiempo_transcurrido)
            tiempo_finU = 1209600 - tiempo_sec
            tiempo_diasU = int(tiempo_finU // 86400)
            tiempo_transcurrido = tiempo_actual - birth
            tiempo_finV = 7776000 - tiempo_sec
            tiempo_diasV = int(tiempo_finV // 86400)
        yield [pyRTOS.timeout(1)]

pyRTOS.add_task(pyRTOS.Task(task_on, name="task_on", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(task_slide, name="task_slide", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(task_time, name="task_time", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(task_button_on, name="task_button_on", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(task_button_slide, name="task_button_slide", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(task_button_time, name="task_button_time", mailbox=True))

pyRTOS.start()