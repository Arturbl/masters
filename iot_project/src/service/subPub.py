import time


class SubPub:

    def __init__(self, client):
        self.client = client

    def on_connect(self, userdata, flags, return_code):
        if return_code == 0:
            print("connected")
        else:
            print("could not connect, return code:", return_code)


    def send_message(self, topic, msgArray):
        msg_count = 0
        try:
            while msg_count < len(msgArray):
                time.sleep(1)
                result = self.client.publish(topic, msgArray[msg_count])
                status = result[0]
                if status == 0:
                    print("Message " + str(msgArray[msg_count]) + " is published to topic " + topic)
                else:
                    print("Failed to send message to topic " + topic)
                msg_count += 1
        finally:
            self.client.loop_stop()