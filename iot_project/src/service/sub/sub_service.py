import time
import src.model.payloaddto as payloaddto


class SubService:
    BROKER_HOSTNAME = "localhost"
    PORT = 1883

    def __init__(self, client):
        self.client = client
        self.thread_listener = True
        self.payload_dto = payloaddto.PayloadDto()

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            print("Subscriber listening on port %d" % self.PORT)
            self.client.subscribe("idc/fitness")
            return
        print("Could not connect, return code: ", return_code)

    def on_message(self, client, userdata, body):
        self.payload_dto.parse(body.payload.decode("utf-8"))
        print("Received message: " + str(self.payload_dto))
        prediction = self.processor.process(self.payload_dto)
        self.db_handler_service.save(self.payload_dto, prediction)

    def setup_mqtt_client(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.BROKER_HOSTNAME, self.PORT)
        self.client.loop_start()

    def cleanup_and_exit(self):
        print("Cleaning up and exiting.")
        self.thread_listener = False
        self.client.loop_stop()

    def mqtt_thread(self):
        self.setup_mqtt_client()
        while self.thread_listener:
            time.sleep(1)
