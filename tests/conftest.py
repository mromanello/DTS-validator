from typing import Dict, Optional, Tuple
import pytest 
import json
import os
import requests
import logging
from uritemplate import URITemplate
from dts_validator.client import DTS_API, DTS_Navigation

LOGGER = logging.getLogger()
SKIP_MOCK_TESTS_MESSAGE = 'A remote DTS API is provided; skipping tests on mock/example data'

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
#   Fixtures for DTS API client and Entry Endpoint  #
#####################################################

def load_mock_data(basedir, filename) -> Dict:
    # load the mock data from a JSON file stored in `tests/data/`
    mock_data_path = os.path.join(basedir, f'data/{filename}.json')

    with open(mock_data_path, 'r') as file:
        mock_request = json.load(file)
    LOGGER.info(f'Loaded mock response from file {mock_data_path}')
    return mock_request

@pytest.fixture(scope='module')
def dts_client(request) -> Optional[DTS_API]:
    if request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        return DTS_API(entry_endpoint_uri)
    else:
        return None    

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # the JSON response comes from the remote DTS API being tested
            pytest.param('entry/entry_invalid_response', marks=pytest.mark.xfail), # example of an invalid response
            pytest.param('entry/entry_old_response', marks=pytest.mark.xfail), # response corresp. to an older version of DTS specs 
            'entry/entry_docs_response', # JSON response from the documentation examples
        ]
)
def entry_endpoint_response(request, dts_client: Optional[DTS_API]) -> Optional[Dict]:
    """
    This fixture returns a DTS Entry endpoint response. If no URI is provided
    via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        return dts_client._entry_endpoint_json
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        return load_mock_data(tests_dir, request.param)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)
        
#####################################################
#     Response fixtures for Collection Endpoint     #
#####################################################

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # the JSON response comes from the remote DTS API being tested
            'collection/collection_docs_response_root', # JSON response from the documentation examples (all collections)
        ]
)      
def collection_endpoint_response_root(request, dts_client: Optional[DTS_API]) -> Optional[Dict]:
    """
    This fixture returns a DTS Collection endpoint response, when no collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        dts_client.collections()
        return dts_client._collection_endpoint_json
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        return load_mock_data(tests_dir, request.param)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # the JSON response comes from the remote DTS API being tested
            'collection/collection_docs_response_one', # JSON response from the documentation examples (one collection)
        ]
)      
def collection_endpoint_response_one(request, dts_client: Optional[DTS_API]) -> Optional[Dict]:
    """
    This fixture returns a DTS Collection endpoint response, when one collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        one_collection_id = dts_client.collections()[-1].id # let's take always the last one
        # TODO: use the URITemplate declared in `Resource.collection` rather than the one 
        # declared by the Entry endpoint
        return dts_client.collections(id=one_collection_id)._json # get full collection metadata from the API
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        return load_mock_data(tests_dir, request.param)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # the JSON response comes from the remote DTS API being tested
            'collection/collection_docs_response_readable', # JSON response from the documentation examples (one readable collection)
        ]
)      
def collection_endpoint_response_readable(request, dts_client: Optional[DTS_API]) -> Optional[Dict]:
    """
    This fixture returns a DTS Collection endpoint response, when one collection is selected. 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource_id = dts_client.get_one_resource().id
        return dts_client.collections(id=readable_resource_id)._json
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        return load_mock_data(tests_dir, request.param)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)

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
def navigation_endpoint_response_down_one(
    request,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[DTS_Navigation], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when querying the root of a `Resource` (`down=1`). 
    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource = dts_client.get_one_resource()
        return dts_client.navigation(resource=readable_resource, down=1)
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        navigation = DTS_Navigation(load_mock_data(tests_dir, request.param))
        return (navigation, None)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # the JSON response comes from the remote DTS API being tested
            'navigation/navigation_docs_response_down_two', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_down_two(
    request,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[DTS_Navigation], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when retrieving an array
    of all `Citable Unit`s for a given `Resource` down to the second level of the `Resource`;s
    citation tree (`&down=2`).  

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource = dts_client.get_one_resource()
        # TODO: here we should check the maxCiteDepth in the default CitationTree
        return dts_client.navigation(resource=readable_resource, down=2)
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        navigation = DTS_Navigation(load_mock_data(tests_dir, request.param))
        return (navigation, None)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'navigation/navigation_docs_response_ref', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_ref(
    request,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[DTS_Navigation], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when retrieving the entire
    citation subtree for a `Citable Unit` of a given `Resource` (`?ref=<citable_unit)id>&down=-1`). 
    See DTS API specs, section "Navigation Endpoint", example #3.

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on mock/example data will be
    performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource = dts_client.get_one_resource()
        
        # first we need to get all resource's citable units
        navigation_obj, response_obj = dts_client.navigation(resource=readable_resource, down=1)
        
        # then we pick one citable unit, by default the last one
        # and use it to query its subtree
        target_citable_unit = navigation_obj.citable_units[-1]
        return dts_client.navigation(resource=readable_resource, reference=target_citable_unit, down=-1)
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        navigation = DTS_Navigation(load_mock_data(tests_dir, request.param))
        return (navigation, None)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            'navigation/navigation_docs_response_top_ref_down_two', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_top_ref_down_two(
    request,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[DTS_Navigation], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when retrieving
    the citation subtree (children + grand-children) for a `Citable Unit` of a given 
    `Resource` (`?ref=<citable_unit)id>&down=2`). 
    See DTS API specs, section "Navigation Endpoint", example #4.

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on
    mock/example data will be performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource = dts_client.get_one_resource()
        
        # first we need to get all resource's citable units
        navigation_obj, response_obj = dts_client.navigation(resource=readable_resource, down=1)
        
        # then we pick one citable unit, by default the last one
        # and use it to query its subtree
        target_citable_unit = navigation_obj.citable_units[-1]
        return dts_client.navigation(resource=readable_resource, reference=target_citable_unit, down=2)
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        navigation = DTS_Navigation(load_mock_data(tests_dir, request.param))
        return (navigation, None)
    else:
        pytest.skip(SKIP_MOCK_TESTS_MESSAGE)


@pytest.fixture
def navigation_endpoint_response_low_ref_down_one(
    request,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[Dict], requests.models.Response]:
    pass

@pytest.fixture
def navigation_endpoint_response_range_plus_down(
    request,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[Dict], requests.models.Response]:
    pass

#####################################################
#     Response fixtures for Document Endpoint       #
#####################################################

@pytest.fixture
def document_endpoint_response_ref(
    request,
    navigation_endpoint_response_down_one: Tuple[Optional[DTS_Navigation], requests.models.Response]
):
    navigation_obect, response_object = navigation_endpoint_response_down_one

    if response_object:
        pass
    else:
        tests_dir = os.path.dirname(request.module.__file__)
        document = load_mock_data(tests_dir, request.param)
        return (document, None)