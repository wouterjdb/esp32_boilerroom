from umqtt.robust import MQTTClient


def connect(client_id, broker_ip, broker_port):
    """
    This function sets up the connection to the MQTT broker.

    Args:
        client_id: The unique id of the client used when sending messages
            to the MQTT broker
        broker_ip: The ip-address (or hostname) of the MQTT broker. Make
            sure that the ip-address is static.
        broker_port: port used by the MQTT broker to receive messages.

    Returns:
        A connected MQTT client object

    Exception:
        Print message. Reset machine.

    """
    try:
        print("(Re)connecting to MQTT broker...", end=" ")
        client = MQTTClient(client_id, broker_ip, port=broker_port)
        client.connect()
        print("[Connected]")

        return client

    except:
        print("Due to an MQTT error the board will reset.")
        machine.reset()
