import time


class PubService:

    def __init__(self, client):
        self.client = client

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            print("connected")
            return
        print("could not connect, return code:", return_code)

    def send_message(self, topic, payload):
        try:
            time.sleep(1)
            result = self.client.publish(topic, payload.format())
            status = result[0]
            if status == 0:
                print("Message " + str(payload) + " sent")
                return
            print("Failed to send message " + topic)
        finally:
            self.client.loop_stop()