import logging
import requests
from typing import Dict, Tuple, Optional
from dts_validator.client import DTS_Navigation

LOGGER = logging.getLogger(__name__)

# TODO: test for invalid combinations of parameters, as per specs
# For each invalid combination, the correspondent HTTP exception should be raised
# `with pytest.raises` is your friend

def test_document_resource_response_validity(document_endpoint_response_resource: Tuple[Optional[str], requests.models.Response]):
    document_text, response_object = document_endpoint_response_resource
    response_object.raise_for_status()
    assert isinstance(document_text, str)
    assert response_object
    LOGGER.info(document_text)

def test_document_ref_response_validity(document_endpoint_response_ref: Tuple[Optional[str], requests.models.Response]):
    document_text, response_object = document_endpoint_response_ref
    response_object.raise_for_status()
    assert isinstance(document_text, str)
    assert response_object
    LOGGER.info(document_text)
    # TODO test for <dts:wrapper> not empty

def test_document_range_response_validity(document_endpoint_response_range: Tuple[Optional[str], requests.models.Response]):
    document_text, response_object = document_endpoint_response_range
    response_object.raise_for_status()
    assert isinstance(document_text, str)
    assert response_object
    LOGGER.info(document_text)
    # TODO test for <dts:wrapper> not empty
