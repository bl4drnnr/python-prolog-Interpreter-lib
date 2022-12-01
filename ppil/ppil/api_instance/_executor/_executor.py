import os
import subprocess
from inspect import getsourcefile
from os.path import abspath


class Executor:
    def __init__(self, json_parser, json_format_checker):
        self._json_parser = json_parser
        self._json_format_checker = json_format_checker

    def execute_code(self, code):
        current_directory = abspath(getsourcefile(lambda: 0))
        current_directory = current_directory.split('/')
        current_directory = '/'.join(current_directory[:-1])

        os.chmod(f"{current_directory}/source_script.pl", 0o777)
        os.chmod(f"{current_directory}/executor.sh", 0o777)

        source_code = code['data']
        source_script_file = open(f"{current_directory}/source_script.pl", 'w')

        if isinstance(source_code, str):
            serialized_program = source_code.replace('\n', '').strip()
        else:
            json_data = self._json_format_checker.check_json_format(code)
            serialized_program = self._json_parser.parse_json(json_data)

        source_script_file.write(serialized_program)

        val = subprocess.check_call(f"{current_directory}/executor.sh", shell=True)

        return 'success'
