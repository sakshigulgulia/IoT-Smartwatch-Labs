import network, socket, time
from machine import Pin, I2C
import ssd1306
import ntptime

rtc = machine.RTC()
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
oled_flag = 0
time_flag = 0

def wlan_connect():
    wlan = network.WLAN(network.STA_IF)     # create station interface
    wlan.active(True)
    wlan.scan()                             # activate the interface
    if not wlan.isconnected():
        wlan.connect('Columbia University', '') # connect to an AP
        while not wlan.isconnected():
            pass
    ip_addr = wlan.ifconfig()               # get the interface's IP/netmask/gw/DNS addresses
    return ip_addr

def display_on(msg):
    display.fill(0)
    display.text(msg, 0, 10)
    display.show()

def display_off():
    display.fill(0)
    display.show()

def time_display():
    display.fill(0)
    t = rtc.datetime()
    display.text('{} - {} - {}' .format(t[2], t[1], t[0]), 0, 0)
    display.text('{} : {} : {}' .format(t[4], t[5], t[6]), 0, 10)
    display.show()

def msg_display(msg):
    display.fill(0)
    display.text(msg, 0, 0)
    display.show()  

def init_server():
    address = socket.getaddrinfo(ip_addr[0], 80)[0][-1]
    print(address)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(2)
    return s

def receive(s):
    sock, send_addr = s.accept()
    print('client connected from :' + str(send_addr))
    request = str(sock.recv(4096))
    #print('http '+ request)
    return sock, request

print('C0')
ip_addr = wlan_connect()
print(ip_addr)
print('C1')
s = init_server()
print('server')
while True:
    sock, request = receive(s)
    try:
        print(request)
        if 'msg' in request:
            msg = request.split('/?msg')[1].split('HTTP')[0]
            msg = msg.replace('%20', ' ')
            print(msg)
            response = 'Hello from Huzzah'

            if 'display' in msg and 'on' in msg:
                oled_flag = 1
                response = 'OLED Display On'

            elif 'display' in msg and 'off' in msg:
                oled_flag = 0
                time_flag = 0
                response = 'OLED Display Off'

            elif 'display' in msg and 'time' in msg:
                time_flag = 1
                oled_flag = 1
                response = 'OLED Displaying Time'

            else:
                time_flag = 0
                oled_flag = 0
                msg_display(msg)
                time.sleep(2)
                response = 'Invalid Message'
            
            success_response = "HTTP/1.1 200 OK\r\n\r\n%s" % response
            sock.send(str.encode(success_response))

            if oled_flag and not time_flag:
                display_on("display on")

            if not oled_flag and not time_flag:
                display_off()

            if time_flag and oled_flag:
                ntptime.settime()
                current_time_list = list(rtc.datetime())
                if current_time_list[4] >= 4:
                    current_time_list[4] = current_time_list[4] - 4
                else:
                    current_time_list[4] = 24 + current_time_list[4] - 4
                rtc.datetime(tuple(current_time_list))
                for i in range (100):
                    time_display()
                    time.sleep(0.5)

    except:
        failed_response = "HTTP/1.1 404 Error\r\n\r\n!"
        sock.send(str.encode(failed_response))
    finally:
        sock.close()