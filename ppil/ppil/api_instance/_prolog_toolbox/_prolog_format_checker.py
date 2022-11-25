class PrologFormatChecker:
    def __init__(self):
        self._prolog_string = []
        self._parsed_json = {}

    def check_prolog_format(self, prolog_string):
        self._prolog_string = prolog_string['data'].replace('\n', '').strip().split('.')[:-1]
        return self._check_items(self._prolog_string)

    def _check_items(self, data):
        for elem in self._prolog_string:
            if ':-' in elem:
                [fact_head, fact_body] = elem.split(':-')
                fact_name = fact_head.split('(')[0]

        return self._parsed_json
