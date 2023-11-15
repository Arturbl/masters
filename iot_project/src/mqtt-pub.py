import paho.mqtt.client as mqtt
from service.subPub import SubPub


BROKER_HOSTNAME = "localhost"
PORT = 1883
client = mqtt.Client("Client1")
subPub = SubPub(client)


def build_messages():
    return [
        '[{"model":"training-DT"},'
        '{"acceleration_x":0.2650,'
        '"acceleration_y":-0.7814,'
        '"acceleration_z":-0.0076,"'
        'gyro_x":-0.0590,'
        '"gyro_y":0.0325,'
        '"gyro_z":-2.9296}]'
    ]


def main():
    client.on_connect = subPub.on_connect
    client.connect(BROKER_HOSTNAME, PORT)
    client.loop_start()

    messages = build_messages()

    subPub.send_message("idc/fitness", messages)

if __name__ == '__main__':
    main()