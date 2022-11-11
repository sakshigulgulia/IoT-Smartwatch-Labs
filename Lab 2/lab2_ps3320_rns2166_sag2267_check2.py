from machine import Pin
import time


led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)

def debounce(button):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    cur_value = button.value()
    active = 0
    while active < 20:
        if button.value() != cur_value:
            active += 1
        else:
            active = 0
        time.sleep_ms(1)

    if button.value():
        led.value(0)
    else:
        led.value(1)




while True:
    button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=debounce)
