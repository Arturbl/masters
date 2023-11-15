import paho.mqtt.client as mqtt
from service.pub import on_connect, send_message


BROKER_HOSTNAME = "localhost"
PORT = 1883


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
    client = mqtt.Client("Client1")
    client.on_connect = on_connect
    client.connect(BROKER_HOSTNAME, PORT)
    client.loop_start()

    messages = build_messages()

    send_message(client, "idc/fitness", messages)

if __name__ == '__main__':
    main()