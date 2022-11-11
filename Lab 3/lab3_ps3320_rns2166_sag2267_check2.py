from machine import Pin, I2C, ADC
import time
import ssd1306

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

rtc = machine.RTC()
rtc.datetime((2022, 10, 1, 0, 0, 0, 0, 0))

button_a = Pin(2, Pin.IN, Pin.PULL_UP)
button_b = Pin(12, Pin.IN, Pin.PULL_UP)
adcpin = ADC(0)

current_position = 3

def w_display():
    display.fill(0)
    t = rtc.datetime()
    display.text('{} - {} - {}' .format(t[2], t[1], t[0]), 0, 0)
    display.text('{} : {} : {}' .format(t[4], t[5], t[6]), 0, 10)
    display.show()

def determine_position(button_a):
    global current_position
    #debounce
    active = 0
    while active < 20:
        if button_a.value() == 0:
            active += 1
        else:
            return
        
        if active == 20:
            global a_flag
            a_flag = 1
            break
        time.sleep_ms(1)

    #update position
    if a_flag:
        current_position = 4 + (current_position % 3)
    
def increment_value(button_b):
    global current_position
    #debounce
    active = 0
    while active < 20:
        if button_b.value() == 0:
            active += 1
        else:
            return
            
        if active == 20:
            global b_flag
            b_flag = 1
            break
        time.sleep_ms(1)

    #increment time values
    if b_flag:
        time_tuple = list(rtc.datetime())
        time_tuple[current_position] += 1
        rtc.datetime(tuple(time_tuple))

#interrupts
button_a.irq(trigger=Pin.IRQ_FALLING, handler=determine_position)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=increment_value)

while True:
    w_display()
    display.contrast(adcpin.read())
    time.sleep_ms(500)
