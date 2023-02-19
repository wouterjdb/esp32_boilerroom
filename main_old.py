"""Implements a HD44780 character LCD connected via NodeMCU GPIO pins."""
from machine import Pin
from utime import sleep, ticks_ms
from nodemcu_gpio_lcd import GpioLcd
import onewire
import ds18x20

# Wiring used for this example:
#
#  1 - Vss (aka Ground) - Connect to one of the ground pins on you NodeMCU board.
#  2 - VDD - Connect to 3V
#  3 - VE (Contrast voltage) - I'll discuss this below
#  4 - RS (Register Select) connect to D0 (as per call to GpioLcd)
#  5 - RW (Read/Write) - connect to ground
#  6 - EN (Enable) connect to D1 (as per call to GpioLcd)
#  7 - D0 - leave unconnected
#  8 - D1 - leave unconnected
#  9 - D2 - leave unconnected
# 10 - D3 - leave unconnected
# 11 - D4 - connect to D2 (as per call to GpioLcd)
# 12 - D5 - connect to D3 (as per call to GpioLcd)
# 13 - D6 - connect to D4 (as per call to GpioLcd)
# 14 - D7 - connect to D5 (as per call to GpioLcd)
# 15 - A (BackLight Anode) - Connect to 3V
# 16 - K (Backlight Cathode) - Connect to Ground
#
# On 14-pin LCDs, there is no backlight, so pins 15 & 16 don't exist.
#
# The Contrast line (pin 3) typically connects to the center tap of a
# 10K potentiometer, and the other 2 legs of the 10K potentiometer are
# connected to pins 1 and 2 (Ground and VDD)


def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    lcd = GpioLcd(
        rs_pin=Pin(23),
        enable_pin=Pin(22),
        d4_pin=Pin(21),
        d5_pin=Pin(19),
        d6_pin=Pin(18),
        d7_pin=Pin(5),
        num_lines=2,
        num_columns=16,
    )
    lcd.putstr("Jacob en Tobias\nzijn lief!")
    sleep(2)
    lcd.clear()
    count = 0
    while True:
        sleep(1)
        lcd.move_to(0, 0)
        count += 1
        ds_sensor.convert_temp()
        for i, rom in enumerate(roms):
            lcd.putstr(
                f"T_{str(i)} = " + str(round(ds_sensor.read_temp(rom), 1)) + " C\n"
            )
            print(rom)
        print("counting further...")


ds_pin = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print("Found DS devices: ", roms)
test_main()
