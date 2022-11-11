import network
import urequests

from machine import Pin, I2C
import ssd1306


i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

def display_coordinates(latitude,longitude):
    display.fill(0)
    display.text('Lat:', 0, 0)
    display.text(latitude, 50, 0)
    display.text('Lon:', 0, 10)
    display.text(longitude, 50, 10)
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

display_coordinates(latitude, longitude)
