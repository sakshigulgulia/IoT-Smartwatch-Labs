from machine import Pin, I2C
from machine import SPI
import time, math
import ssd1306

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

spi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, mode=Pin.OUT, value=1)
#default init positions
x_pos = 64
y_pos = 16

def init():
    time.sleep_ms(50)
    #set adxl345
    cs.value(0)
    spi.write(b'\x31\x07')#set bits for register 0x31
    cs.value(1)
    time.sleep_ms(50)
    cs.value(0)
    spi.write(b'\x2D\x08')#set bits for register 0x2D
    cs.value(1)
    time.sleep_ms(50)
    cs.value(0)
    spi.write(b'\x2C\x0A')#set bits for register 0x2C
    cs.value(1)
    time.sleep_ms(50)
    cs.value(0)
    spi.write(b'\x2E\x00')#set bits for register 0x2E
    cs.value(1)
    time.sleep_ms(50)
    cs.value(0)
    spi.write(b'\x38\x00')#set bits for register 0x38
    cs.value(1)
    time.sleep_ms(50)

def read_adxl_and_get_coordinates():
    cs.value(0)
    x2 = spi.read(5, 0xf3)
    cs.value(1)

    cs.value(0)
    y2 = spi.read(5, 0xf5)
    cs.value(1)

    return x2[1], y2[1]
    

def w_display(x, y):
    global x_pos
    global y_pos
    display.fill(0) 
    display.text('Hello', x_pos, y_pos)
    display.show()

    if 0 < x < 128:
        x_pos += x
        
    if x > 128:
        x_pos -= 256 - x
        
    if 0 < y < 128:
        y_pos += y
        
    if y > 128:
        y_pos -= 256 - y
        
    if x_pos >= 128:
        x_pos = 0
    if x_pos < 0:
        x_pos = 128
    if y_pos >= 32:
        y_pos = 0
    if y_pos < 0:
        y_pos = 32
    time.sleep(0.001)
    
def main():
    init()
    while True:
        p_x, p_y = read_adxl_and_get_coordinates()
        w_display(p_x, p_y)

if __name__ == '__main__':
    main()