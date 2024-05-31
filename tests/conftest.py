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

######################################
#     JSON schema-related fixtures   #
######################################

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

@pytest.fixture()
def collection_response_schema(request) -> Dict:
    """
    This fixture returns the JSON schema to validate responses of a DTS Collection endpoint.
    """
    test_dir = os.path.dirname(request.module.__file__)
    schema_path = '../schemas/collection_response.schema.json'

    with open(os.path.join(test_dir, schema_path), 'r') as schema_file:
        json_schema = json.load(schema_file)
    return json_schema

######################################
#     Responses-related fixtures     #
######################################

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None
            pytest.param('invalid_entry_response', marks=pytest.mark.xfail), # example of an invalid response
            pytest.param('old_entry_response', marks=pytest.mark.xfail), # response corresp. to an older version of DTS specs 
            'entry_response_from_docs', # example response from the documentation
        ]
)
def entry_endpoint_response(request):
    """
    This fixture returns a DTS Entry endpoint response. If no URI is provided
    via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they are skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        req  = requests.get(entry_endpoint_uri)
        assert 'application/ld+json' in req.headers['Content-Type']
        return req.json()
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            # load the mock data from a JSON file stored in `tests/data/`
            test_dir = os.path.dirname(request.module.__file__)
            mock_data_path = os.path.join(test_dir, f'data/{request.param}.json')
            
            with open(mock_data_path, 'r') as file:
                mock_request = json.load(file)
            LOGGER.info(f'Loaded mock response from file {mock_data_path}')
            return mock_request
        else:
            pytest.skip()
        
