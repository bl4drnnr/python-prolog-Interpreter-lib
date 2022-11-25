from ._api_response_handler import \
    WrongFactFormat, \
    WrongJsonFormat, \
    WrongPrologFormat, \
    WrongConditionFormat, \
    ApiResponse, \
    ExecutionError
from ._executor import Executor

from ._json_toolbox import JsonParser, JsonFormatChecker
from ._prolog_toolbox import PrologParser, PrologFormatChecker


class Converter:
    def __init__(self):
        self._output_program = None
        self._execute_result = None

        self._json_format_checker = JsonFormatChecker()
        self._prolog_format_checker = PrologFormatChecker()

        self._json_parser = JsonParser()
        self._prolog_parser = PrologParser()

    def json_to_prolog(self, input_json_data):
        try:
            json_data = self._json_format_checker.check_json_format(input_json_data)
            self._output_program = self._json_parser.parse_json(json_data)

            return ApiResponse(self._output_program, 200)
        except WrongJsonFormat as wjf:
            return wjf
        except WrongFactFormat as wff:
            return wff
        except WrongConditionFormat as wcf:
            return wcf
        except Exception as e:
            return ApiResponse(str(e), 500)

    def prolog_to_json(self, input_prolog_data):
        try:
            prolog_data = self._prolog_format_checker.check_prolog_format(input_prolog_data)
            self._output_program = self._prolog_parser.parse_prolog(prolog_data)

            return ApiResponse(self._output_program, 200)
        except WrongPrologFormat as wpf:
            return wpf
        except Exception as e:
            return ApiResponse(str(e), 500)

    def json_execute(self, input_json_data):
        try:
            json_data = self._json_format_checker.check_json_format(input_json_data)
            prolog_data = self._json_parser.parse_json(json_data)
            self._execute_result = Executor.execute_code(prolog_data)

            return ApiResponse(self._execute_result, 200)
        except ExecutionError as ee:
            return ee
        except Exception as e:
            return ApiResponse(str(e), 500)

    def prolog_execute(self, input_prolog_data):
        try:
            prolog_data = self._prolog_format_checker.check_prolog_format(input_prolog_data)
            self._execute_result = Executor.execute_code(prolog_data)

            return ApiResponse(self._execute_result, 200)
        except ExecutionError as ee:
            return ee
        except Exception as e:
            return ApiResponse(str(e), 500)
