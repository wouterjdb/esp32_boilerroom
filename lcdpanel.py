from machine import Pin
from nodemcu_gpio_lcd import GpioLcd
from settings import rs_pin_nr, enable_pin_nr, d4_pin_nr, d5_pin_nr, d6_pin_nr, d7_pin_nr, num_lines, num_columns

class LCDPanel():
    def __init__(self):
        self.lcd = GpioLcd(rs_pin=Pin(rs_pin_nr),
                      enable_pin=Pin(enable_pin_nr),
                      d4_pin=Pin(d4_pin_nr),
                      d5_pin=Pin(d5_pin_nr),
                      d6_pin=Pin(d6_pin_nr),
                      d7_pin=Pin(d7_pin_nr),
                      num_lines=num_lines,
                      num_columns=num_columns)
    
    def write(self, text):
        self.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(text)        
        
    def clear(self):
        self.lcd.clear()