import json
from json import JSONEncoder
import requests
from flask import Flask, jsonify, request
import threading
import src.model.payloaddto as payloaddto
import src.service.database.db_handler_service as dbhandler


class PayloadDtoEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, payloaddto.PayloadDto):
            return o.__dict__
        return super().default(o)


class Processor:
    MODEL = "training-DT"

    def __init__(self):
        self.app = Flask(__name__)
        self.register_routes()
        threading.Thread(target=self.run_flask_app).start()
        self.db_handler_service = dbhandler.DatabaseHandlerService()

    def run_flask_app(self):
        self.app.run(host='localhost', port=8081)

    def register_routes(self):
        self.app.add_url_rule('/login', 'login', self.validate_user, methods=['POST'])

    def process(self, payload):
        model_component = {"model": self.MODEL}
        payload_component = payload.__dict__
        json_payload = json.dumps([model_component, payload_component])
        url = 'http://localhost:8000/predict'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get("prediction")
        return None

    def validate_user(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        result = self.db_handler_service.validate_user_password(username, password)
        if result is not None:
            return jsonify(True)
        else:
            return jsonify(False)

