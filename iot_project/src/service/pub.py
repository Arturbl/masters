import time


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)


def send_message(client, topic, msgArray):
    msg_count = 0
    try:
        while msg_count < len(msgArray):
            time.sleep(1)
            result = client.publish(topic, msgArray[msg_count])
            status = result[0]
            if status == 0:
                print("Message " + str(msgArray[msg_count]) + " is published to topic " + topic)
            else:
                print("Failed to send message to topic " + topic)
            msg_count += 1
    finally:
        client.loop_stop()