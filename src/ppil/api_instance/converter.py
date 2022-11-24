from .api_response_handler import WrongFactFormat, WrongJsonFormat, WrongPrologFormat, ApiResponse
from .format_checker import FormatChecker
from .json_parser import JsonParser
from .prolog_parser import PrologParser


class Converter:
    def __init__(self):
        self._output_program = None
        self._format_checker = FormatChecker()
        self._json_parser = JsonParser()
        self._prolog_parser = PrologParser()

    def json_to_prolog(self, input_json_data):
        try:
            json_data = self._format_checker.check_json_format(input_json_data)
            self._output_program = self._json_parser.parse_json(json_data)

            return ApiResponse(self._output_program, 200)
        except WrongJsonFormat:
            return WrongJsonFormat()
        except WrongFactFormat:
            return WrongFactFormat()
        except Exception as e:
            return ApiResponse(str(e), 500)

    def prolog_to_json(self, input_prolog_data):
        try:
            prolog_data = self._format_checker.check_prolog_format(input_prolog_data)
            self._output_program = self._prolog_parser.parse_prolog(prolog_data)

            return ApiResponse(self._output_program, 200)
        except WrongPrologFormat:
            return WrongPrologFormat()
        except Exception as e:
            return ApiResponse(str(e), 500)

    def json_execute(self, input_json_data):
        try:
            return ApiResponse(self._output_program, 200)
        except Exception as e:
            return ApiResponse(str(e), 500)

    def prolog_execute(self, input_prolog_data):
        try:
            return ApiResponse(self._output_program, 200)
        except Exception as e:
            return ApiResponse(str(e), 500)
