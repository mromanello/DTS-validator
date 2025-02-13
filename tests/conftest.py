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
SKIP_NO_CITABLE_UNITS_MESSAGE = 'No citable units found in the navigation object'

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
    mock_data_path = os.path.join(basedir, f'data/{filename}')

    with open(mock_data_path, 'r') as file:
        if mock_data_path.endswith('json'):
            mock_request = json.load(file)
        else:
            raise
        LOGGER.info(f'Loaded mock response from file {mock_data_path}')
    return mock_request

@pytest.fixture(scope='module')
def dts_client(request: pytest.FixtureRequest) -> Optional[DTS_API]:
    if request.config.getoption('--entry-endpoint') is not None:
        entry_endpoint_uri = request.config.getoption('--entry-endpoint')
        return DTS_API(entry_endpoint_uri)
    else:
        return None    

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # the JSON response comes from the remote DTS API being tested
            pytest.param('entry/entry_invalid_response.json', marks=pytest.mark.xfail), # example of an invalid response
            pytest.param('entry/entry_old_response.json', marks=pytest.mark.xfail), # response corresp. to an older version of DTS specs 
            'entry/entry_docs_response.json', # JSON response from the documentation examples
        ]
)
def entry_endpoint_response(request: pytest.FixtureRequest, dts_client: Optional[DTS_API]) -> Optional[Dict]:
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
            'collection/collection_docs_response_root.json', # JSON response from the documentation examples (all collections)
        ]
)      
def collection_endpoint_response_root(request: pytest.FixtureRequest, dts_client: Optional[DTS_API]) -> Optional[Dict]:
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
            'collection/collection_docs_response_one.json', # JSON response from the documentation examples (one collection)
        ]
)      
def collection_endpoint_response_one(request: pytest.FixtureRequest, dts_client: Optional[DTS_API]) -> Optional[Dict]:
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
            'collection/collection_docs_response_readable.json', # JSON response from the documentation examples (one readable collection)
        ]
)      
def collection_endpoint_response_readable(request: pytest.FixtureRequest, dts_client: Optional[DTS_API]) -> Optional[Dict]:
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
            'navigation/navigation_docs_response_down_one.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_down_one(
    request: pytest.FixtureRequest,
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
            'navigation/navigation_docs_response_down_two.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_down_two(
    request: pytest.FixtureRequest,
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
            'navigation/navigation_docs_response_ref.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_ref(
    request: pytest.FixtureRequest,
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
        
        # if the Resource has citable units, we pick by default the last one
        # and use it to query its subtree
        if navigation_obj.citable_units:
            target_citable_unit = navigation_obj.citable_units[-1]
            return dts_client.navigation(resource=readable_resource, reference=target_citable_unit, down=-1)
        # otherwise we skip the test
        else:
            pytest.skip(f'{navigation_obj.resource}: {SKIP_NO_CITABLE_UNITS_MESSAGE}')
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
            'navigation/navigation_docs_response_top_ref_down_two.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_top_ref_down_two(
    request: pytest.FixtureRequest,
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
        
        # if the Resource has citable units, we pick by default the last one
        # and use it to query its subtree
        if navigation_obj.citable_units:
            target_citable_unit = navigation_obj.citable_units[-1]
            return dts_client.navigation(resource=readable_resource, reference=target_citable_unit, down=2)
        else:
            pytest.skip(f'{navigation_obj.resource}: {SKIP_NO_CITABLE_UNITS_MESSAGE}')
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
            'navigation/navigation_docs_response_low_ref_down_one.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_low_ref_down_one(
    request: pytest.FixtureRequest,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[Dict], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response, when retrieving
    the direct children of a low-level `Citable Unit` (= two levels deep) of a given 
    `Resource` (`?ref=<citable_unit)id>&down=1`). 
    See DTS API specs, section "Navigation Endpoint", example #5.

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on
    mock/example data will be performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        # TODO: finish implementation
        pytest.skip('Not implemented yet; depends on changes to `client.DTS_API`')
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
            'navigation/navigation_docs_response_range_plus_down.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_range_plus_down(
    request: pytest.FixtureRequest,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[Dict], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response
    when retrieving an array of `CitableUnit`s in a specified range, including
    the direct children of the specified start and end points (`?start=<citable_unit_1>&end=<citable_unit_2>&down=1`).
    See DTS API specs, section "Navigation Endpoint", example #6.

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on
    mock/example data will be performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource = dts_client.get_one_resource()
        
        # first we need to get all resource's citable units
        navigation_obj, response_obj = dts_client.navigation(resource=readable_resource, down=1)
        
        # if the Resource has citable units, we define a range of refs (first-last),
        # and use this range to query the navigation endpoint
        if navigation_obj.citable_units:
            start_ref = navigation_obj.citable_units[0]
            end_ref = navigation_obj.citable_units[-1]
            return dts_client.navigation(
                resource=readable_resource,
                start=start_ref,
                end=end_ref,
                down=1
            )
        else:
            pytest.skip(f'{navigation_obj.resource}: {SKIP_NO_CITABLE_UNITS_MESSAGE}')
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
            #'navigation/navigation_docs_response_range_plus_down.json', # JSON response from the documentation examples
        ]
)
def navigation_endpoint_response_range(
    request: pytest.FixtureRequest,
    dts_client: Optional[DTS_API]
) -> Tuple[Optional[Dict], requests.models.Response]:
    """
    This fixture returns a DTS Navigation endpoint response
    when retrieving an array of `CitableUnit`s in a specified range
    (`?start=<citable_unit_1>&end=<citable_unit_2`).

    If no URI is provided via the `--entry-endpoint` parameter, a number of tests on
    mock/example data will be performed (otherwise they will be skipped).
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        readable_resource = dts_client.get_one_resource()
        
        # first we need to get all resource's citable units
        navigation_obj, response_obj = dts_client.navigation(resource=readable_resource, down=1)
        
        # if the Resource has citable units, we define a range of refs (first-last),
        # and use this range to query the navigation endpoint
        if navigation_obj.citable_units:
            start_ref = navigation_obj.citable_units[0]
            end_ref = navigation_obj.citable_units[-1]
            return dts_client.navigation(
                resource=readable_resource,
                start=start_ref,
                end=end_ref
            )
        else:
            pytest.skip(f'{navigation_obj.resource}: {SKIP_NO_CITABLE_UNITS_MESSAGE}')
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        navigation = DTS_Navigation(load_mock_data(tests_dir, request.param))
        return (navigation, None)
    else:
        pytest.skip()

#####################################################
#     Response fixtures for Document Endpoint       #
#####################################################

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            #'navigation/navigation_docs_response_range_plus_down.json', # JSON response from the documentation examples
        ]
)
def document_endpoint_response_resource(
    request: pytest.FixtureRequest,
    dts_client: Optional[DTS_API],
) -> Tuple[Optional[str], requests.models.Response]:
    """_summary_

    :param request: _description_
    :type request: pytest.FixtureRequest
    :param dts_client: _description_
    :type dts_client: Optional[DTS_API]
    :return: _description_
    :rtype: Tuple[Optional[str], requests.models.Response]
    """
    # use remote API for tests
    if request.param is None and dts_client is not None:
        one_resource = dts_client.get_one_resource()
        return dts_client.document(
            resource=one_resource
        )
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        document = load_mock_data(tests_dir, request.param)
        return (document, None)
    else:
        pytest.skip()

@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            #'navigation/navigation_docs_response_range_plus_down.json', # JSON response from the documentation examples
        ]
)
def document_endpoint_response_range(
    request: pytest.FixtureRequest,
    dts_client: Optional[DTS_API],
    navigation_endpoint_response_range: Tuple[Optional[DTS_Navigation], requests.models.Response]
) -> Tuple[Optional[str], requests.models.Response]:
    """_summary_

    :param request: _description_
    :type request: pytest.FixtureRequest
    :param dts_client: _description_
    :type dts_client: Optional[DTS_API]
    :param navigation_endpoint_response_down_one: _description_
    :type navigation_endpoint_response_down_one: Tuple[Optional[DTS_Navigation], requests.models.Response]
    :return: _description_
    :rtype: _type_
    """
    navigation_object, response_object = navigation_endpoint_response_range

    # use remote API for tests
    if response_object and dts_client is not None:
        assert navigation_object
        assert navigation_object.start and navigation_object.end and navigation_object.resource
        return dts_client.document(
            resource=navigation_object.resource,
            start=navigation_object.start,
            end=navigation_object.end
        )
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        document = load_mock_data(tests_dir, request.param)
        return (document, None)
    else:
        pytest.skip()

    
@pytest.fixture(
        scope='module',
        params=[
            pytest.param(None), # response is None,
            #'navigation/navigation_docs_response_range_plus_down.json', # JSON response from the documentation examples
        ]
)
def document_endpoint_response_ref(
    request: pytest.FixtureRequest,
    dts_client: Optional[DTS_API],
    navigation_endpoint_response_down_one: Tuple[Optional[DTS_Navigation], requests.models.Response]
) -> Tuple[Optional[str], requests.models.Response]:
    """_summary_

    :param request: _description_
    :type request: pytest.FixtureRequest
    :param dts_client: _description_
    :type dts_client: Optional[DTS_API]
    :param navigation_endpoint_response_down_one: _description_
    :type navigation_endpoint_response_down_one: Tuple[Optional[DTS_Navigation], requests.models.Response]
    :return: _description_
    :rtype: _type_
    """
    navigation_object, response_object = navigation_endpoint_response_down_one

    # use remote API for tests
    if response_object and dts_client is not None:
        assert navigation_object
        # if the Resource has no citable units (this may happen) we skip the test 
        if navigation_object.citable_units:
            one_reference = navigation_object.citable_units[0]
            return dts_client.document(
                resource=navigation_object.resource,
                reference=one_reference
            )
        else:
            pytest.skip(f'{navigation_object.resource}: {SKIP_NO_CITABLE_UNITS_MESSAGE}')
    # use mock/example data for tests
    elif request.param and dts_client is None:
        tests_dir = os.path.dirname(request.module.__file__)
        document = load_mock_data(tests_dir, request.param)
        return (document, None) 
    else:
        pytest.skip()