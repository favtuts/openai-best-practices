import os
import requests
from openapi_spec_validator import validate_spec_url

def test_blueprint_testing_test(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'testing', 'test')
    response = requests.get(endpoint)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "I'm the test endpoint from blueprint_testing."

def test_blueprint_testing_plus(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'testing', 'plus')
    payload = {'number': 5}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Your result is: '10'"

def test_blueprint_testing_minus(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'testing', 'minus')
    payload = {'number': 1000}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Your result is: '0'"

def test_swagger_specification(host):
    endpoint = os.path.join(host, 'api', 'swagger.json')
    validate_spec_url(endpoint)
    # use https://editor.swagger.io/ to fix issues