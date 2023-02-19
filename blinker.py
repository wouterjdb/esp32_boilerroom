from machine import Pin
import time

import settings

try:
    led = Pin(settings.GPIO_PIN_LED, Pin.OUT)
except:
    print(e)
    blink(5)
    machine.reset() 

def blink(times, freq=5, duty=0.5):
    """
    Function that blinks the onboard led (halts the program while
    doing so).
    
    Args:
        times (int): Number of times to blink the led.
        freq (int): Blinking freqency in Herz (default: 10)
        duty (float): Blinking duty cycle in fractions (default: 0.5)
    
    Returns:
        Nothing
    """
    try:
        for i in range(times):        
            led.value(1)
            time.sleep(duty / freq)
            led.value(0)
            time.sleep((1 - duty) / freq)
    except Exception as e:
        print(e)
        machine.reset() 
