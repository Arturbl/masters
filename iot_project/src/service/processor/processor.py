import json
from json import JSONEncoder
import requests
import src.model.payloaddto as payloaddto


class PayloadDtoEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, payloaddto.PayloadDto):
            return o.__dict__
        return super().default(o)


class Processor:
    PROCESSOR_HOST = 'localhost'
    PROCESSOR_PORT = '8000'

    MODEL = "training-DT"

    def process(self, payload):
        model_component = {"model": self.MODEL}
        payload_component = payload.__dict__

        json_payload = json.dumps([model_component, payload_component])

        url = f'http://{self.PROCESSOR_HOST}:{self.PROCESSOR_PORT}/predict'
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json_payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return result.get("prediction")
        return None
