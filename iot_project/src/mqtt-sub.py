import threading
import paho.mqtt.client as mqtt
from service.sub_service import SubService
import time


class MqttSubscriber:

    def __init__(self):
        self.client = mqtt.Client("Client2")
        self.sub_service = SubService(self.client)
        self.mqtt_listener = threading.Thread(target = self.sub_service.mqtt_thread)

    def run(self):
        self.mqtt_listener.start()
        self.loop()
        self.sub_service.cleanup_and_exit()
        self.mqtt_listener.join()

    def loop(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    mqtt_listener = MqttSubscriber()
    mqtt_listener.run()
