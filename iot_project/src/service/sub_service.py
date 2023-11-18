import time

global THREAD_LISTENER
global CLIENT


class SubService:

    def __init__(self, client):
        self.client = client
        self.thread_listener = True
        self.broker_hostname = "localhost"
        self.port = 1883

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            print("MQTT Subscriber listening on port %d" % self.port)
            self.client.subscribe("idc/fitness")
            return
        print("Could not connect, return code: ", return_code)

    def on_message(self, client, userdata, message):
        print("Received message: ", str(message.payload.decode("utf-8")))

    def setup_mqtt_client(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_hostname, self.port)
        self.client.loop_start()

    def cleanup_and_exit(self):
        print("Cleaning up and exiting.")
        self.thread_listener = False
        self.client.loop_stop()

    def mqtt_thread(self):
        self.setup_mqtt_client()
        while self.thread_listener:
            time.sleep(1)
