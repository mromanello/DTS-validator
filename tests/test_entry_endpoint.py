import pytest
import logging
from dts_validator.validation import validate_json, validate_uri_template

LOGGER = logging.getLogger()

def test_json_response_validity(entry_endpoint_response : dict, entry_response_schema : dict):
    """Validates the JSON response of a remote DTS Entry endpoint against its schema.

    :param entry_endpoint_response: The JSON returned by the DTS Entry endpoint
    :type entry_endpoint_response: dict
    :param entry_response_schema: The JSON schema for the DTS Entry endpoint
    :type entry_response_schema: dict
    """
    validate_json(entry_endpoint_response, entry_response_schema) # this will test appropriate assertions

def test_json_response_uri_templates(entry_endpoint_response : dict):
    """
    Checks the URI templates contained in the JSON response of a remote DTS Entry endpoint
    to ensure they contain the mandatory parameters as per specs. 

    :param entry_endpoint_response: The JSON returned by the DTS Entry endpoint
    :type entry_endpoint_response: dict
    :raises URITemplateMissingParameter: If a mandatory parameter is missing from the URI template
    """
    
    expected_parameters = {
        'collection': ['id', 'nav'], # NOTE: see question to tech. comm. about `page` param
        'navigation': ['resource', 'ref', 'start', 'end'], # if compliancy_level == 1, `start` and `end` must be there 
        'document': ['resource', 'ref', 'start', 'end'] # if compliancy_level == 1, `start` and `end` must be there
    }
    
    for property in expected_parameters.keys():  
        params = expected_parameters[property]
        uri_template = entry_endpoint_response[property]
        validate_uri_template(uri_template, template_name=property, required_parameters=params)