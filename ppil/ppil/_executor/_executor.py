import os
import subprocess
from inspect import getsourcefile
from os.path import abspath

from ppil.ppil._api_response_handler import ExecutionError


class Executor:
    def __init__(self, json_parser, json_format_checker):
        self._json_parser = json_parser
        self._json_format_checker = json_format_checker
        self._current_directory = None

    def _set_current_directory(self):
        current_directory = abspath(getsourcefile(lambda: 0))
        current_directory = current_directory.split('/')
        self._current_directory = '/'.join(current_directory[:-1])

    def execute_code(self, code):
        if not code.get('query'):
            raise ExecutionError(response='No set query.')

        self._set_current_directory()

        prolog_source_path = f"{self._current_directory}/source_script.pl"
        executor_path = f"{self._current_directory}/executor.sh"

        source_code = code['data']
        source_script_file = open(prolog_source_path, 'w+')

        os.chmod(prolog_source_path, 0o700)
        os.chmod(executor_path, 0o700)

        if isinstance(source_code, str):
            serialized_program = source_code.replace('\n', '').strip()
        else:
            json_data = self._json_format_checker.check_json_format(code)
            serialized_program = self._json_parser.parse_json(json_data)

        serialized_program = '.\n'.join(serialized_program.split('.'))
        source_script_file.write(serialized_program)
        source_script_file.close()

        code_query = code.get('query')
        execution_result = subprocess.run(
            f"{executor_path} %s %s" % (f"'{code_query}'", prolog_source_path),
            shell=True,
            stdout=subprocess.PIPE
        )

        return execution_result.stdout.decode('utf-8')
