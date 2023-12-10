import paho.mqtt.client as mqtt
import time
from service.pub.pub_service import PubService
from service.pub.csv_handler_service import CsvHandlerService


class MqttPublisher:
    BROKER_HOSTNAME = "localhost"
    PORT = 1883

    def __init__(self):
        self.client = mqtt.Client("Client1")
        self.sub_pub = PubService(self.client)
        self.csv_handler_service = CsvHandlerService()

    def build_client(self):
        self.client.on_connect = self.sub_pub.on_connect
        self.client.connect(self.BROKER_HOSTNAME, self.PORT)
        self.client.loop_start()

    def build_messages(self):
        while True:
            payload = self.csv_handler_service.generate_payload_instance()
            self.sub_pub.send_message("idc/fitness", payload)
            time.sleep(1)

    def run(self):
        self.build_client()
        self.build_messages()


if __name__ == '__main__':
    mqtt_publisher = MqttPublisher()
    mqtt_publisher.run()
