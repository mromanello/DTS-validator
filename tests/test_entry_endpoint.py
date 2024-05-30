import pytest
import logging
import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError

LOGGER = logging.getLogger()

def test_json_response_validity(entry_endpoint_response : dict, entry_response_schema : dict):
    """Validates the JSON response of a remote DTS Entry endpoint against its schema.

    :param entry_endpoint_response: The JSON returned by the DTS Entry endpoint (fixture)
    :type entry_endpoint_response: dict
    :param entry_response_schema: The JSON schema for the DTS Entry endpoint (fixture)
    :type entry_response_schema: dict
    """
    try:
        assert validate(entry_endpoint_response, entry_response_schema) is None
        LOGGER.info('JSON schema and JSON response are valid.')
    except ValidationError as e:
        # TODO catpure more specific exceptions from `jsonschema.validate()`
        LOGGER.error('Either the JSON schema or the JSON object are invalid.')
        raise e
    
@pytest.mark.skip(reason="TODO: needs to be implemented")
def test_json_response_templates():
    pass