import logging
from dts_validator.validation import validate_collection_response, validate_uri_template, check_required_property

LOGGER = logging.getLogger()

def test_json_response_validity(collection_endpoint_response_root : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection when no collection is selected.

    :param collection_endpoint_response_root: The JSON returned by the DTS Collection endpoint (Fixture)
    :type collection_endpoint_response_root: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint (Fixture)
    :type collection_response_schema: dict
    """
    validate_collection_response(collection_endpoint_response_root, collection_response_schema)

def test_one_collection_response_validity(collection_endpoint_response_one : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection endpoint when one collection is selected.
    
    :param collection_endpoint_response_one: The JSON returned by the DTS Collection endpoint (Fixture)
    :type collection_endpoint_response_one: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint (Fixture)
    :type collection_response_schema: dict
    """
    validate_collection_response(collection_endpoint_response_one, collection_response_schema)

def test_readable_collection_response_validity(collection_endpoint_response_readable : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection endpoint when one readable collection is selected (@type==Resource).    

    :param collection_endpoint_response_readable: The JSON returned by the DTS Collection endpoint (Fixture)
    :type collection_endpoint_response_readable: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint (Fixture)
    :type collection_response_schema: dict"""
    # TODO: use the response.schema.json instead
    validate_collection_response(collection_endpoint_response_readable, collection_response_schema)


def test_readable_collection_response_additional_required_properties(collection_endpoint_response_readable : dict) -> None:
    """Checks for the presence of additional required properties of a remote
    DTS Collection endpoint response when one readable collection is selected (@type==Resource). 

    :param collection_endpoint_response_readable: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_readable: dict
    """

    expected_parameters = {
        'collection': ['nav'],  # see https://github.com/distributed-text-services/specifications/pull/251
        'navigation': ['ref', 'start', 'end'],  # if compliancy_level == 1, `start` and `end` must be there
        'document': ['ref', 'start', 'end']  # if compliancy_level == 1, `start` and `end` must be there
    }
    print(collection_endpoint_response_readable)
    
    for prpty in expected_parameters.keys():
        # before checking the content of the URI template, let's make sure
        # that is present in the JSON response
        check_required_property(collection_endpoint_response_readable, prpty)
        
        # let's now check that it declares all expected parameters
        uri_template = collection_endpoint_response_readable[prpty]
        params = expected_parameters[prpty]
        validate_uri_template(uri_template, template_name=prpty, required_parameters=params)


# TODO: add test for parent collection