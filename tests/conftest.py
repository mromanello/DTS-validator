from typing import Dict, Optional, Tuple
import pytest 
import json
import os
import requests
import logging
from uritemplate import URITemplate
from dts_validator.client import DTS_API, DTS_Navigation

LOGGER = logging.getLogger()

def pytest_addoption(parser):
    parser.addoption(
        "--entry-endpoint", action="store"
    )

######################################
#     Fixtures for JSON schemas      #
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

@pytest.fixture()
def navigation_response_schema(request) -> Dict:
    """
    This fixture returns the JSON schema to validate responses of a DTS Navigation endpoint.
    """
    test_dir = os.path.dirname(request.module.__file__)
    schema_path = '../schemas/navigation_response.schema.json'

    with open(os.path.join(test_dir, schema_path), 'r') as schema_file:
        json_schema = json.load(schema_file)
    return json_schema


#####################################################
#     Response fixtures for Entry Endpoint          #
#####################################################

def load_mock_data(basedir, filename) -> Dict:
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
            pytest.param('entry/entry_invalid_response', marks=pytest.mark.xfail), # example of an invalid response
            pytest.param('entry/entry_old_response', marks=pytest.mark.xfail), # response corresp. to an older version of DTS specs 
            'entry/entry_docs_response', # JSON response from the documentation examples
        ]
)
def entry_endpoint_response(request) -> Optional[Dict]:
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

#####################################################
#     Response fixtures for Collection Endpoint     #
#####################################################

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'collection/collection_docs_response_root', # JSON response from the documentation examples (all collections)
        ]
)      
def collection_endpoint_response_root(request) -> Optional[Dict]:
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
            'collection/collection_docs_response_one', # JSON response from the documentation examples (one collection)
        ]
)      
def collection_endpoint_response_one(request) -> Optional[Dict]:
    """
    This fixture returns a DTS Collection endpoint response, when one collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        one_collection_id = client.collections()[-1].id # let's take always the last one
        return client.collections(id=one_collection_id)._json # get full collection metadata from the API
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
            'collection/collection_docs_response_readable', # JSON response from the documentation examples (one readable collection)
        ]
)      
def collection_endpoint_response_readable(request) -> Optional[Dict]:
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

#####################################################
#     Response fixtures for Navigation Endpoint     #
#####################################################

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'navigation/navigation_docs_response_down_one', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_down_one(request) -> Tuple[Optional[Dict], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when querying the root of a `Resource` (`down=1`). 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        readable_resource = client.get_one_resource()
        navigation_obj, response_obj = client.navigate(resource=readable_resource, down=1)
        return (navigation_obj._json, response_obj)
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return (mock_request, None)
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'navigation/navigation_docs_response_down_two', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_down_two(request) -> Tuple[Optional[Dict], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when retrieving an array
    of all `Citable Unit`s for a given `Resource` down to the second level of the `Resource`;s
    citation tree (`&down=2`).  

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        readable_resource = client.get_one_resource()
        # TODO: here we should check the maxCiteDepth in the default CitationTree
        navigation_obj, response_obj = client.navigate(resource=readable_resource, down=2)
        if navigation_obj:
            return (navigation_obj._json, response_obj)
        else:
            return (None, response_obj)
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return(mock_request, None)
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'navigation/navigation_docs_response_ref', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_ref(request) -> Tuple[Optional[Dict], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when retrieving the entire
    citation subtree for a `Citable Unit` of a given `Resource` (`?ref=<citable_unit)id>&down=-1`). 
    See DTS API specs, section "Navigation Endpoint", example #3.

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    if request.param is None and request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        client = DTS_API(entry_endpoint_uri)
        readable_resource = client.get_one_resource()
        # first we need to get all resource's citable units
        navigation_obj, response_obj = client.navigate(resource=readable_resource, down=1)
        # then we pick one citable unit, by default the last one
        # and use it to query its subtree
        target_citable_unit = navigation_obj.citable_units[-1]
        if navigation_obj:
            navigation_obj, response_obj = client.navigate(
                resource=readable_resource,
                reference=target_citable_unit,
                down=-1
            )
            return (navigation_obj._json, response_obj)
        else:
            return (None, response_obj)
    elif request.config.getoption('--entry-endpoint') is not None:
        pytest.skip('A remote DTS API is provided; skipping mock tests')
    else:
        if request.param:
            tests_dir = os.path.dirname(request.module.__file__)
            mock_request = load_mock_data(tests_dir, request.param)            
            return(mock_request, None)
        else:
            pytest.skip('No remote DTS API is provided; skipping live tests')

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            #'navigation/navigation_docs_response_down_two', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_top_ref_down_one(request):
    pass


"""
TODO: create the following fixtures
ERROR tests/test_navigation_endpoint.py::test_navigation_top_ref_down_one_response_validity
ERROR tests/test_navigation_endpoint.py::test_navigation_low_ref_down_one_response_validity
ERROR tests/test_navigation_endpoint.py::test_navigation_range_plus_down_response_validity
"""

#####################################################
#     Response fixtures for Document Endpoint       #
#####################################################