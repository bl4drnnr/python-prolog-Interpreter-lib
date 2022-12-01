import os
import subprocess
from inspect import getsourcefile
from os.path import abspath

from ppil.ppil._api_response_handler import ExecutionError


def _wrap_facts(prolog_program):
    prolog_program = prolog_program.split('.')
    updated_prolog_program = []

    for item in prolog_program:
        if ':-' in item:
            condition_part = item.split(':-')[1]
            updated_prolog_program.append(
                item.replace(
                    condition_part,
                    f'forall(({condition_part}), format("~q ~a ~n", [X, Y])), halt'
                )
            )
        else:
            updated_prolog_program.append(item)

    return [item for item in updated_prolog_program if len(item) > 0]


class Executor:
    def __init__(self, json_parser, json_format_checker):
        self._json_parser = json_parser
        self._json_format_checker = json_format_checker
        self._current_directory = None

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

        # Here is what I am going to do
        # If it's pure prolog, split it by dot
        # Iterate it and find fact, wrap it

        # For JSON first convert to prolog and do steps above

        # Also allow user to send list of queries
        # What to do with variables
        if isinstance(source_code, str):
            serialized_program = _wrap_facts(source_code)
        else:
            json_data = self._json_format_checker.check_json_format(code)
            serialized_program = self._json_parser.parse_json(json_data)

        serialized_program = '.\n'.join(serialized_program) + '.\n'
        source_script_file.write(serialized_program)
        source_script_file.close()

        code_query = code.get('query')
        execution_result = subprocess.run([
            'swipl', '-q', '-g', code_query, '-t', 'halt', prolog_source_path
        ])

        return execution_result.stdout.decode('utf-8')

    def _set_current_directory(self):
        current_directory = abspath(getsourcefile(lambda: 0))
        current_directory = current_directory.split('/')
        self._current_directory = '/'.join(current_directory[:-1])

