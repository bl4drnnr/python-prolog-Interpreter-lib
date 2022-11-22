from flask import Flask, request


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
        self._request_data = request

    def _json_to_prolog(self):
        self._request_data = request.get_json()

    def _json_execute(self):
        self._request_data = request.get_json()

    def _prolog_execute(self):
        self._request_data = request

    def run(self, **kwargs):
        self._app = Flask(__name__)

        self._add_endpoint('/prolog-to-json', 'prolog-to-json', self._prolog_to_json, methods=['POST'])
        self._add_endpoint('/json-to-prolog', 'json-to-prolog', self._json_to_prolog, methods=['POST'])
        self._add_endpoint('/json-execute', 'json-execute', self._json_execute, methods=['POST'])
        self._add_endpoint('/prolog-execute', 'prolog-execute', self._prolog_execute, methods=['POST'])

        self._app.run(**kwargs)
