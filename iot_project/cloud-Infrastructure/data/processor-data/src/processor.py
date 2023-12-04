import json

import requests
from flask import Flask, request, Response, jsonify
from datetime import datetime

import db_handler_service as dbHandler
import csv_handler_service as csvHandler
import results_analyser as resultsAnalyser

MODEL = "training-DT"

app = Flask(__name__)
db_handler_service = dbHandler.DatabaseHandlerService()


@app.route('/processor', methods=['POST'])
def process_data():
    body = request.get_json()
    model_component = {"model": MODEL}
    payload_component = body
    json_payload = json.dumps([model_component, payload_component])
    url = 'http://172.100.10.14:8000/predict'
    headers = {'Content-Type': 'application/json'}
    with requests.post(url, data=json_payload, headers=headers) as response:
        if response.status_code == 200:
            activity_prediction = response.json()['prediction']
            result = db_handler_service.save(json_payload, activity_prediction)
            return json_payload if result else "Database not recheable"
    return "Could not process data"


@app.route('/login', methods=['POST'])
def validate_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    result = db_handler_service.validate_user_password(username, password)
    return build_response(result)


@app.route('/history', methods=['GET'])
def get_history():
    dateBegin = request.args.get('dateBegin')
    dateEnd = request.args.get('dateEnd')
    if not dateBegin or not dateEnd:
        return jsonify({'error': 'Missing date parameters'}), 400
    try:
        dateBegin = datetime.strptime(dateBegin, '%Y-%m-%d')
        dateEnd = datetime.strptime(dateEnd, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    results = db_handler_service.get_history(dateBegin, dateEnd)
    if results:
        analysed_results = resultsAnalyser.analyse(results)
        return {
            "total": len(results),
            "result": analysed_results
        }
    return {
        "error": "Could not find results for the given dates"
    }


@app.route('/health', methods=['GET'])
def health():
    result = db_handler_service.health()
    return build_response(result)


def build_response(response):
    return Response(json.dumps(response), mimetype='application/json').data


if __name__ == '__main__':
    csvHandler.main()
    app.run(host='0.0.0.0', port=8081)
