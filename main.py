import machine
from utime import sleep, ticks_ms

print("Waiting to boot ESP32...", end="")
sleep(3)
print("[Done]")

try:
    from utime import sleep, ticks_ms
    import gc

    gc.collect()

    from machine import Pin
    import esp

    esp.osdebug(None)
    import math

    from blinker import blink
    import settings
    import sensors
    import wifi
    import blinker
    from robust import MQTTClient
except:
    machine.reset()

try:
    pin_hp_in11 = Pin(settings.GPIO_PIN_HP_IN11, mode=Pin.OUT)
    pin_hp_in12 = Pin(settings.GPIO_PIN_HP_IN12, mode=Pin.OUT)
except:
    machine.reset()


def mqtt_message_received(topic, msg):
    """
    This function handles incoming MQTT messages

    Args:
        topic: Topic name
        msg: The message

    Returns:
        Nothing

    Exception:
        Nothing, board will be reset
    """
    try:
        print("message received %s %s" % (topic, msg))
        if topic.decode() == settings.MQTT_TOPIC_HP_IN11:
            if msg.decode() == "ON":
                pin_hp_in11.on()
            else:
                pin_hp_in11.off()
        elif topic.decode() == settings.MQTT_TOPIC_HP_IN12:
            if msg.decode() == "ON":
                pin_hp_in12.on()
            else:
                pin_hp_in12.off()
        else:
            print("Uknown topic")
    except Exception as e:
        machine.reset()


def main():
    """
    Main function to run when script is executed.
    """
    try:
        station = wifi.connect(settings.SSID, settings.PASSWORD)

        print("Creating MQTT client...", end="")
        client = MQTTClient(
            settings.MQTT_CLIENT_ID,
            settings.MQTT_BROKER_IP,
            settings.MQTT_BROKER_PORT,
            ssl=False,
        )
        print("[Done]")

        print("Setting callback...", end="")
        client.set_callback(mqtt_message_received)
        print("[Done]")

        print("Connecting MQTT client...", end="")
        client.connect()
        print("[Done]")

        print("Subscribing to topic %s..." % settings.MQTT_TOPIC_HP_IN11, end="")
        client.subscribe(settings.MQTT_TOPIC_HP_IN11)
        print("[Done]")

        print("Subscribing to topic %s..." % settings.MQTT_TOPIC_HP_IN12, end="")
        client.subscribe(settings.MQTT_TOPIC_HP_IN12)
        print("[Done]")

        print("Initializing Sensor Array...", end="")
        sensorarray = sensors.SensorArray(settings.ds_pin_nr)
        print("[Done]")

    except:
        machine.reset()

    while True:
        try:
            blink(1)

            # Check if WiFi is (still) connected. If not, reconnect.
            if not station.isconnected():
                print("Wifi connection lost, reconnecting...", end="")
                station = wifi.connect(settings.SSID, settings.PASSWORD)
                print("[Connected]")

            try:
                print("Checking messages...", end="")
                client.check_msg()
                print("[Done]")
            except OSError:
                machine.reset()

            for i in range(1, len(settings.sensors) + 1):
                sensor_value = sensorarray.get_value(i)
                print("Sensor %s = %s" % (i, str(sensor_value)))

                if not math.isnan(sensor_value):
                    client.publish(
                        settings.MQTT_TOPIC_T + str(i), b"%s" % str(sensor_value)
                    )

            sleep(settings.time_delay)
        except:
            machine.reset()


main()
