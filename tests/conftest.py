from typing import Dict
import pytest 
import json
import os
import requests
import logging
from uritemplate import URITemplate
from dts_validator import DTS_API

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

def load_mock_data(basedir, filename):
    # load the mock data from a JSON file stored in `tests/data/`
    mock_data_path = os.path.join(basedir, f'data/{filename}.json')

    with open(mock_data_path, 'r') as file:
        mock_request = json.load(file)
    LOGGER.info(f'Loaded mock response from file {mock_data_path}')
    return mock_request

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None
            pytest.param('entry_invalid_response', marks=pytest.mark.xfail), # example of an invalid response
            pytest.param('entry_old_response', marks=pytest.mark.xfail), # response corresp. to an older version of DTS specs 
            'entry_docs_response', # example response from the documentation
        ]
)
def entry_endpoint_response(request):
    """
    This fixture returns a DTS Entry endpoint response. If no URI is provided
    via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        return client._entry_endpoint_json
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return mock_request
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'collection_docs_response_root', # example response from the documentation (all collections)
        ]
)      
def collection_endpoint_response_root(request):
    """
    This fixture returns a DTS Collection endpoint response, when no collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        client.collections()
        collection_req = client._collection_endpoint_json
        return collection_req
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return mock_request
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')


@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'collection_docs_response_one', # example response from the documentation (one collection)
        ]
)      
def collection_endpoint_response_one(request):
    """
    This fixture returns a DTS Collection endpoint response, when one collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        one_collection_id = client.collections()[-1].id
        return client.collections(id=one_collection_id)._json
    elif request.param is not None and request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return mock_request
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'collection_docs_response_readable', # example response from the documentation (one readable collection)
        ]
)      
def collection_endpoint_response_readable(request):
    """
    This fixture returns a DTS Collection endpoint response, when one collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        readable_resource_id = client.get_one_resource().id
        return client.collections(id=readable_resource_id)._json
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return mock_request
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')