from flask import Flask, request
from .json_converter import JsonConverter

AVAILABLE_ENDPOINTS = ['prolog-to-json', 'json-to-prolog', 'json-execute', 'prolog-execute']


class ApiInstance:
    def __init__(self, **configs):
        self._app = None
        self._request_data = None
        self._configs(**configs)

    def _configs(self, **configs):
        for config, value in configs:
            self._app.config[config.upper()] = value

    def _add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, *args, **kwargs):
        self._app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def _prolog_to_json(self):
        self._request_data = request.get_json()
        response = JsonConverter.prolog_to_json(self._request_data)
        return response.response, response.status_code

    def _json_to_prolog(self):
        self._request_data = request.get_json()
        response = JsonConverter.json_to_prolog(self._request_data)
        return response.response, response.status_code

    def _json_execute(self):
        self._request_data = request.get_json()
        response = JsonConverter.json_execute(self._request_data)
        return response.response, response.status_code

    def _prolog_execute(self):
        self._request_data = request.get_json()
        response = JsonConverter.prolog_execute(self._request_data)
        return response.response, response.status_code

    def run(self, **kwargs):
        self._app = Flask(__name__)

        for endpoint in AVAILABLE_ENDPOINTS:
            self._add_endpoint(f'/{endpoint}', endpoint, eval(f'self._{endpoint.replace("-", "_")}'), methods=['POST'])

        self._app.run(**kwargs)
