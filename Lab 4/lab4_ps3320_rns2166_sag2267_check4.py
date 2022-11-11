import network
import urequests

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('Columbia University', '') # connect to an AP
wlan.config('mac')      # get the interface's MAC address
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)         # activate the interface

response = urequests.get('http://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key=A5KGLPT9MN7KX869&status=Good Evening!')

