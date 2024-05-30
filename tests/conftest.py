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
def entry_response_schema(request) -> Dict:
    """
    This fixture returns the JSON schema to validate responses of a DTS Entry endpoint.
    """
    test_dir = os.path.dirname(request.module.__file__)
    schema_path = '../schemas/entry_response.schema.json'

    with open(os.path.join(test_dir, schema_path), 'r') as schema_file:
        json_schema = json.load(schema_file)
    return json_schema

@pytest.fixture(scope='module', params=[None, 'invalid', 'docs-example'])
def entry_endpoint_response(request):
    """
    This fixture returns a DTS Entry endpoint response. If no URI is provided
    via the `--entry-endpoint` parameter, a number of tests on mock data will be
    performed (otherwise they are skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        return requests.get(entry_endpoint_uri).json()
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        return request.param
