from machine import Pin
import utime

pin0 = Pin(0, Pin.OUT)
pin2 = Pin(2, Pin.OUT)
pin0.value(1)
pin2.value(1)
while True:
		pin0.value(0)
		pin2.value(0)
		utime.sleep_ms(500)
		pin0.value(1)
		pin2.value(1)
		utime.sleep_ms(500)


		pin2.value(0)
		utime.sleep_ms(500)
		pin2.value(1)
		utime.sleep_ms(500)

		pin2.value(0)
		utime.sleep_ms(500)
		pin2.value(1)
		utime.sleep_ms(500)

		pin2.value(0)
		utime.sleep_ms(500)
		pin2.value(1)
		utime.sleep_ms(500)

		pin2.value(0)
		utime.sleep_ms(500)
		pin2.value(1)
		utime.sleep_ms(500)


	



    

