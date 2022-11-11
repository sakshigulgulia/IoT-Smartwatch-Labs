import network
import urequests

from machine import Pin, I2C
import ssd1306


i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

def display_weather_data(temperature,description):
    display.fill(0)
    display.text('Temp:', 0, 0)
    display.text(temperature, 50, 0)
    display.text('Desc:', 0, 10)
    display.text(description, 50, 10)
    display.show()

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('Columbia University', '') # connect to an AP
wlan.config('mac')      # get the interface's MAC address
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)         # activate the interface

response_1 = urequests.get('http://ip-api.com/json/')
parsed_1 = response_1.json()

lat = parsed_1["lat"]
latitude = str(parsed_1["lat"])
lon = parsed_1["lon"]
longitude = str(parsed_1["lon"])

response_2 = urequests.get('https://api.openweathermap.org/data/2.5/weather?lat={0:f}&lon={1:f}&APPID=b604fee729c84c87fad2cc1c6f47b666'.format(lat,lon))
parsed_2 = response_2.json()
temperature_data = parsed_2["main"]

temperature_kelvin = temperature_data["temp"]
temperature_celsius = temperature_kelvin - 273.15
temperature = str(temperature_celsius)

description_data = parsed_2["weather"]
description = str(description_data[0]['description'])

display_weather_data(temperature,description)
