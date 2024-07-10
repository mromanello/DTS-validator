import pytest
import logging
from dts_validator.validation import validate_collection_response, validate_uri_template, check_required_property

LOGGER = logging.getLogger()

def test_json_response_validity(collection_endpoint_response_root : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection when no collection is selected.

    :param collection_endpoint_response_root: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_root: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint
    :type collection_response_schema: dict
    """
    validate_collection_response(collection_endpoint_response_root, collection_response_schema)

def test_one_collection_response_validity(collection_endpoint_response_one : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection endpoint when one collection is selected.
    
    :param collection_endpoint_response_one: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_one: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint
    :type collection_response_schema: dict
    """
    validate_collection_response(collection_endpoint_response_one, collection_response_schema)

def test_readable_collection_response_validity(collection_endpoint_response_readable : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection endpoint when one readable collection is selected (@type==Resource).    

    :param collection_endpoint_response_readable: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_readable: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint
    :type collection_response_schema: dict"""
    validate_collection_response(collection_endpoint_response_readable, collection_response_schema)

def test_readable_collection_response_additional_required_properties(collection_endpoint_response_readable : dict) -> None:
    """Checks for the presence of additional required properties of a remote
    DTS Collection endpoint response when one readable collection is selected (@type==Resource). 

    :param collection_endpoint_response_readable: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_readable: dict
    """

    # maxCiteDepth is a required property of the citationTree
    # if the Collection is of type Resource (this conditional
    # constraint cannot be checked via the JSON schema)
    citation_trees = collection_endpoint_response_readable['citationTrees']
    for cit_tree in citation_trees:
        check_required_property(cit_tree, 'maxCiteDepth')

    expected_parameters = {
        'collection': ['id', 'nav'], # see https://github.com/distributed-text-services/specifications/pull/251
        'navigation': ['ref', 'start', 'end'], # if compliancy_level == 1, `start` and `end` must be there 
        'document': ['ref', 'start', 'end'] # if compliancy_level == 1, `start` and `end` must be there
    }
    
    for property in expected_parameters.keys():  
        # before checking the content of the URI template, let's make sure
        # that is present in the JSON response
        check_required_property(collection_endpoint_response_readable, property)
        
        # let's now check that it declares all expected parameters
        uri_template = collection_endpoint_response_readable[property]
        params = expected_parameters[property]
        validate_uri_template(uri_template, template_name=property, required_parameters=params)


# TODO: add test for parent collection