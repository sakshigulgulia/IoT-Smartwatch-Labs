from machine import Pin, ADC, PWM
import utime
adcpin = ADC(0)
pin12 = Pin(12)
pin14 = Pin(14)
pwm12 = PWM(pin12)
pwm14 = PWM(pin14)

while True:
	input = adcpin.read()
	utime.sleep_ms(50)
	print(input)
	pwm12.duty(input)
	pwm14.duty(input)
	utime.sleep_ms(50)


	
	

