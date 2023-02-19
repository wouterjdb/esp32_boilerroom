from utime import time, sleep
import machine
import network

def connect(ssid, password, lcd = None):
    """
    This functions sets up the connection to the wireless lan.
    The led will blink slowly while connecting.
    Args:
        ssid (str): Wifi name
        password (str): Wifi password
        lcd (LCDPanel): Optional LCD panel to write status to.
    
    Returns:
        Connected station network.WLAN interface instance
    
    Exception:        
        Returns False        
    """
    try:
        print("Connecting to %s..." % ssid, end="")
        sleep(1)
        
        station = network.WLAN(network.STA_IF)        
        if not station.isconnected() is True:
            
            station.active(True)
            station.connect(ssid, password)
            
            t0 = time()
            
            while station.isconnected() is False:
                t1 = time()

                if (t1-t0) > 30:
                    print("[ERROR]")
                    print("Due the WiFi connection process timing out the board will reset.")

                    machine.reset()

                print(".", end = "")
                sleep(0.2)
                pass

        print("[Connected]")
        sleep(4)

        return station

    except Exception as e:
        print(e)
        print("[ERROR] Connection failed, rebooting in 5s...")
        sleep(5)
        machine.reset()