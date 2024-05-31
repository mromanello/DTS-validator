import pytest
import logging
from uritemplate import URITemplate
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from dts_validator.exceptions import URITemplateMissingParameter

LOGGER = logging.getLogger()

def test_json_response_validity(entry_endpoint_response : dict, entry_response_schema : dict):
    """Validates the JSON response of a remote DTS Entry endpoint against its schema.

    :param entry_endpoint_response: The JSON returned by the DTS Entry endpoint
    :type entry_endpoint_response: dict
    :param entry_response_schema: The JSON schema for the DTS Entry endpoint
    :type entry_response_schema: dict
    """
    try:
        assert validate(entry_endpoint_response, entry_response_schema) is None
        LOGGER.info('JSON schema and JSON response are valid.')
    except ValidationError as e:
        # TODO catpure more specific exceptions from `jsonschema.validate()`
        LOGGER.error('Either the JSON schema or the JSON object are invalid.')
        raise e

def test_json_response_uri_templates(entry_endpoint_response : dict):
    """
    Checks the URI templates contained in the JSON response of a remote DTS Entry endpoint
    to ensure they contain the mandatory parameters as per specs. 

    :param entry_endpoint_response: The JSON returned by the DTS Entry endpoint
    :type entry_endpoint_response: dict
    :raises URITemplateMissingParameter: If a mandatory parameter is missing from the URI template
    """
    properties = ['collection', 'navigation', 'document']
    
    for property in properties:    
        uri_template = URITemplate(entry_endpoint_response[property])
        
        if property == 'collection':
            # expected parameters in `collection`` URI template
            # TODO: double check whether the `page` param is mandatory
            params = ['id', 'page', 'nav']
        elif property == 'navigation':
            # TODO expected parameters in `document`` URI template
            # if compliancy_level == 1, `start` and `end` must be there 
            params = ['resource', 'ref', 'page']
        elif property == 'document':
            # expected parameters in `navigation` URI template
            params = ['resource', 'ref']
        
        for param in params:
            try:
                assert param in list(uri_template.variable_names)
            except AssertionError:
                msg = f'[DTS Entry endpoint] Parameter `{param}` must be contained in the `{property}` URI template {uri_template}'
                LOGGER.error(msg)
                raise URITemplateMissingParameter(msg)