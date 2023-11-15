import threading
import paho.mqtt.client as mqtt
from service.subservice import SubService
import time

CLIENT = mqtt.Client("Client2")

subService = SubService(CLIENT)
mqtt_listener = threading.Thread(target=subService.mqtt_thread)


def loop():
    try:
        print("Script is running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def main():
    mqtt_listener.start()
    loop()
    subService.cleanup_and_exit()
    mqtt_listener.join()


if __name__ == "__main__":
    main()
