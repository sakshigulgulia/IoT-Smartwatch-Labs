from machine import Pin, I2C
from machine import PWM
import time
import ssd1306

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

rtc = machine.RTC()
rtc.datetime((2022, 10, 4, 0, 1, 1, 1, 0))

button_a = Pin(2, Pin.IN, Pin.PULL_UP)
button_b = Pin(12, Pin.IN, Pin.PULL_UP)
button_c = Pin(13, Pin.IN, Pin.PULL_UP)
piezo = PWM(Pin(15))

alarm = [0, 0, 0]
alarm_position = -1
current_position = 3
alarm_flag = 0

def w_display():
    display.fill(0)
    t = rtc.datetime()
    display.text('{} - {} - {}' .format(t[2], t[1], t[0]), 0, 0)
    display.text('{} : {} : {}' .format(t[4], t[5], t[6]), 0, 10)
    display.text('{} : {} : {}' .format(str(alarm[0]), str(alarm[1]), str(alarm[2])), 0, 20)
    display.show()

def determine_position(button_a):
    global alarm_flag, current_position, alarm_position
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
        if not alarm_flag:
            #update watch position
            current_position = 4 + (current_position % 3)

        elif alarm_flag:
            #update alarm position
            alarm_position = (alarm_position + 1) % 3


def increment_value(button_b):
    global alarm_flag, alarm_position, current_position
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
        if not alarm_flag:
            #increment watch time
            time_tuple = list(rtc.datetime())
            time_tuple[current_position] += 1
            rtc.datetime(tuple(time_tuple))
        elif alarm_flag:
            #increment alarm time
            alarm[alarm_position] += 1

def set_watch_mode(button_c):
    global alarm_flag
    #debounce
    active = 0
    while active < 20:
        if button_c.value() == 0:
            active += 1
        else:
            return
        
        if active == 20:
            global c_flag
            c_flag = 1
            break
        time.sleep_ms(1)

    #set watch mode to watch{0} or alarm{1}
    if c_flag:
        alarm_flag = 1 - alarm_flag 
    
def ring_alarm(piezo):
    piezo.freq(60)
    i = 0
    while (i<500):
        display.fill(0)
        display.text('ALARM!!', 0, 20)
        display.show()
        piezo.duty(512)
        time.sleep_ms(1)
        i+=1
    piezo.freq(0)
    piezo.duty(0)
    w_display()

#interrupts
button_a.irq(trigger=Pin.IRQ_FALLING, handler=determine_position)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=increment_value)
button_c.irq(trigger=Pin.IRQ_FALLING, handler=set_watch_mode)

while True:
    w_display()
    if (rtc.datetime()[4]==alarm[0] and rtc.datetime()[5]==alarm[1] and rtc.datetime()[6]==alarm[2]):
        ring_alarm(piezo)
    time.sleep_ms(500)