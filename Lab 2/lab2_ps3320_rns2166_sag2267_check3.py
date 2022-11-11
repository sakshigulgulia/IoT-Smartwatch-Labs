from machine import Pin, ADC, PWM
import utime
import time

global adcpin, button, pwmled, pwmpiezo 

adcpin = ADC(0)
button = Pin(14, Pin.IN, Pin.PULL_UP)
pwmled = PWM(Pin(15))
pwmpiezo = PWM(Pin(2))



def debounceandread(button):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    cur_value = button.value()
    active = 0
    while active < 20:
        if button.value() != cur_value:
            active += 1
        else:
            active = 0
        utime.sleep_ms(1)

    while not button.value():
        input = adcpin.read()
        pwmled.duty(input)
        pwmpiezo.duty(input)
    
    
    pwmled.duty(0)
    pwmpiezo.duty(0)

while True:
    button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=debounceandread)