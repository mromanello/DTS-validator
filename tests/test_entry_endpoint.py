import pytest
import logging
import requests
from jsonschema import validate

LOGGER = logging.getLogger()

def test_json_response(entry_endpoint_response : dict, entry_response_schema : dict):
    """Validates the JSON response of the DTS Entry endpoint against its schema.

    :param entry_endpoint_response: The API response.
    :type entry_endpoint_response: dict
    :param entry_response_schema: The JSON schema for the Entry endpoint.
    :type entry_response_schema: dict
    """
    try:
        assert validate(entry_endpoint_response, entry_response_schema) is None
        LOGGER.info('JSON schema and JSON response are valid.')
    except Exception:
        LOGGER.error('Either the JSON schema or the JSON object are invalid.')