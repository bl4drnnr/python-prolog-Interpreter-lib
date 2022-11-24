JSON_FORMAT = {
    "predicate": {
        "name": "str",
        "arguments": "list"
    },
    "fact": {
        "name": "str",
        "arguments": "list",
        "conditions": "list",
        "joins": "list"
    },
    "list": {
        "name": "str",
        "items": "list"
    }
}
ALLOWED_CONDITIONS = ['and', ',', 'or', ';']
ALLOWED_CONDITIONS_TYPES = ['predicate', 'condition']
CONDITION_SEPARATORS = ['=', '>', 'is', '<', '=<', '>=', '=:=', r'=\=']
AVAILABLE_ENDPOINTS = ['prolog-to-json', 'json-to-prolog', 'json-execute', 'prolog-execute']
