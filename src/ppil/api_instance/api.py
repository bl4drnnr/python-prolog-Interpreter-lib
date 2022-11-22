from flask import Flask


class ApiInstance:
    def __init__(self, **configs):
        self._app = None
        self._configs(**configs)

    def _configs(self, **configs):
        for config, value in configs:
            self._app.config[config.upper()] = value

    def _add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, *args, **kwargs):
        self._app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def _action(self):
        return "Hello World"

    def run(self, **kwargs):
        self._app = Flask(__name__)

        self._add_endpoint('/action', 'action', self._action, methods=['GET'])

        self._app.run(**kwargs)
