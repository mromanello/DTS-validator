from typing import Dict
import pytest 
import json
import os
import requests
import logging

LOGGER = logging.getLogger()

def pytest_addoption(parser):

    parser.addoption(
        "--entry-endpoint", action="store"
    ) 

@pytest.fixture()
def setup(request) -> Dict[str, str]:
    dts_entry_point = request.config.getoption('--entry-endpoint')
    LOGGER.info(f"Testing DTS API at {dts_entry_point}")
    LOGGER.debug(f'Tests configuration: {setup}')
    return {
        'entry_endpoint': dts_entry_point
    }

@pytest.fixture()
def entry_response_schema(request) -> Dict:
    test_dir = os.path.dirname(request.module.__file__)
    schema_path = '../schemas/entry_response.schema.json'

    with open(os.path.join(test_dir, schema_path), 'r') as schema_file:
        json_schema = json.load(schema_file)
    return json_schema

@pytest.fixture()
def entry_endpoint_response(setup):
    try:
        response = requests.get(setup['entry_endpoint']).json()
    except Exception as e:
        raise e
    return response