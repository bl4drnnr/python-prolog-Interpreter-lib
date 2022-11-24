import requests
from src.ppil import ApiInstance


def test_prolog_to_json():
    api = ApiInstance()
    api.run(debug=True)


def test_json_to_prolog():
    api = ApiInstance()
    api.run(debug=True)


def test_json_execute():
    api = ApiInstance()
    api.run(debug=True)


def test_prolog_execute():
    api = ApiInstance()
    api.run(debug=True)
