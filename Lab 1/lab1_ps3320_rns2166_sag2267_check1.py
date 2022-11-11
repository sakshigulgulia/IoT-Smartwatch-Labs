from machine import Pin
import utime

pin0 = Pin(0, Pin.OUT)

while True:
	pin0.value(0)
	utime.sleep_ms(500)
	pin0.value(1)
	utime.sleep_ms(500)
	pin0.value(0)
	utime.sleep_ms(500)
	pin0.value(1)
	utime.sleep_ms(500)
	pin0.value(0)
	utime.sleep_ms(500)
	pin0.value(1)

	utime.sleep_ms(1500)

	pin0.value(0)
	utime.sleep_ms(1000)
	pin0.value(1)
	utime.sleep_ms(1000)
	pin0.value(0)
	utime.sleep_ms(1000)
	pin0.value(1)
	utime.sleep_ms(1000)
	pin0.value(0)
	utime.sleep_ms(1000)
	pin0.value(1)

	utime.sleep_ms(1500)

	pin0.value(0)
	utime.sleep_ms(500)
	pin0.value(1)
	utime.sleep_ms(500)
	pin0.value(0)
	utime.sleep_ms(500)
	pin0.value(1)
	utime.sleep_ms(500)
	pin0.value(0)
	utime.sleep_ms(500)
	pin0.value(1)	

	utime.sleep_ms(3000)