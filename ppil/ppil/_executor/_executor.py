import os
import subprocess
from inspect import getsourcefile
from os.path import abspath

from ppil.ppil._api_response_handler import ExecutionError
from ppil.ppil._variables import EXECUTION_RESULT_SPLITER


def _get_fact_head_and_conditions(fact):
    [head_part, condition_part] = fact.split(':-')
    return [head_part.replace('\n', '').strip(), condition_part.replace('\n', '').strip()]


def _wrap_facts(prolog_program, query):
    prolog_program = prolog_program.split('.')
    updated_prolog_program = []
    query_head = query.split('(')[0]

    for item in prolog_program:
        if ':-' in item:
            [head_part, condition_part] = _get_fact_head_and_conditions(item)
            fact_name = head_part.split('(')[0]

            if query_head == fact_name:
                fact_arguments = head_part[head_part.index('(')+1:-1]
                result_output_pattern = ' '.join([f"~q" for index, item in enumerate(fact_arguments.split(','))])
                result_output_pattern += EXECUTION_RESULT_SPLITER

                if fact_name not in condition_part:
                    replace_condition_part = f'forall(({condition_part}), format("{result_output_pattern}", [{fact_arguments}]))'
                else:
                    replace_condition_part = f'({condition_part}), format("{result_output_pattern}", [{fact_arguments}])'

                updated_prolog_program.append(item.replace(condition_part, replace_condition_part))
            else:
                updated_prolog_program.append(item)

        else:
            updated_prolog_program.append(item)

    return [item for item in updated_prolog_program if len(item) > 0]


class Executor:
    def __init__(self, json_parser, json_format_checker):
        self._json_parser = json_parser
        self._json_format_checker = json_format_checker
        self._current_directory = None

    def execute_code(self, code):
        if not code.get('query') and not isinstance(code.get('query'), list):
            raise ExecutionError(response='No set query or query is not list.')

        self._set_current_directory()

        prolog_source_path = f"{self._current_directory}/source_script.pl"

        source_code = code['data']
        source_code = source_code.replace('\n', '') if isinstance(source_code, str) else source_code

        os.chmod(prolog_source_path, 0o700)

        if not isinstance(source_code, str):
            json_data = self._json_format_checker.check_json_format(code)
            source_code = self._json_parser.parse_json(json_data)
            source_code = source_code.replace('\n', '').strip()

        code_query = code.get('query')
        results = []

        for query in code_query:
            query_arguments = query[query.index('(') + 1:-1].split(',')
            if len(query_arguments) == 0:
                pass

            source_script_file = open(prolog_source_path, 'w+')

            serialized_program = _wrap_facts(source_code, query)
            serialized_program = '.\n'.join(serialized_program) + '.'

            source_script_file.write(serialized_program)
            source_script_file.close()

            execution_result = subprocess.run([
                'swipl', '-q', '-g', query, '-t', 'halt', prolog_source_path
            ], stdout=subprocess.PIPE)
            serialized_result = execution_result.stdout.decode('utf-8').split(EXECUTION_RESULT_SPLITER)[:-1]

            for result in serialized_result:
                res = {}
                for query_index, query_argument in enumerate(query_arguments):
                    res[query_argument.strip()] = result.split(' ')[query_index]
                results.append(res)

        return results

    def _set_current_directory(self):
        current_directory = abspath(getsourcefile(lambda: 0))
        current_directory = current_directory.split('/')
        self._current_directory = '/'.join(current_directory[:-1])
