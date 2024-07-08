import pytest
import logging
from dts_validator import validate_json
from dts_validator.exceptions import URITemplateMissingParameter

LOGGER = logging.getLogger()

def test_json_response_validity(collection_endpoint_response_root : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection when no collection is selected.

    :param collection_endpoint_response_root: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_root: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint
    :type collection_response_schema: dict
    """
    validate_json(collection_endpoint_response_root, collection_response_schema)
    
def test_one_collection_response_validity(collection_endpoint_response_one : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection endpoint when one collection is selected.
    
    :param collection_endpoint_response_one: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_one: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint
    :type collection_response_schema: dict
    """
    validate_json(collection_endpoint_response_one, collection_response_schema)

def test_readable_collection_response_validity(collection_endpoint_response_readable : dict, collection_response_schema : dict):
    """Validates the JSON response of a remote DTS Collection endpoint when one readable collection is selected.    

    :param collection_endpoint_response_readable: The JSON returned by the DTS Collection endpoint
    :type collection_endpoint_response_readable: dict
    :param collection_response_schema: The JSON schema for the DTS Collection endpoint
    :type collection_response_schema: dict"""
    validate_json(collection_endpoint_response_readable, collection_response_schema)


# TODO: test URI templates for a readable collection
# TODO: test for deprecated properties