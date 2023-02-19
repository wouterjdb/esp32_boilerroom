from machine import Pin

import onewire
import ds18x20

import settings

class SensorArray():
    
    def __init__(self, ds_pin_nr):
        self.ds_pin_nr = ds_pin_nr
        self._refresh_onewire()        
        
    def __len__(self):
        return len(self.roms)

    def _refresh_values(self):
        try:
            self.ds_sensor.convert_temp()
        except:
            pass

    def _refresh_onewire(self):
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(self.ds_pin_nr)))
        self.roms = self.ds_sensor.scan()
        #print(self.roms)

    def get_value(self, key):
        self._refresh_onewire()
        self._refresh_values()
        
        if not key in settings.sensors.keys():
            raise KeyError("Sensor with key %s does not exist." % key)

        for i, rom in enumerate(self.roms):
            if settings.sensors[key] == rom:
                try:
                    return float(round(self.ds_sensor.read_temp(rom),1))
                except:
                    return float('NaN')
        
        return float('NaN')         
    
    def get_values(self):
        self._refresh_values()
        
        values = []
        for i, rom in enumerate(self.roms):
            values.append(str(round(self.ds_sensor.read_temp(rom),1)))

        return values
