import pytest
import logging
import requests
from typing import Dict, Tuple
from dts_validator.client import DTS_Navigation
from dts_validator.validation import validate_navigation_response

LOGGER = logging.getLogger(__name__)

def test_navigation_one_down_response_validity(
        navigation_endpoint_response_down_one : Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
    ) -> None:
    """
    Validates the JSON response of a remote DTS Navigation endpoint, when retrieving the top-level
    `Citable Unit`s of a given `Resource` (`&down=1`). 
    See DTS API specs, section "Navigation Endpoint", example #1.

    :param navigation_endpoint_response_down_one: A tuple containing a `DTS_Navigation` object
        and `requests`' response object.
    :type navigation_endpoint_response_down_one: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: The JSON schema for the DTS Navigation endpoint (Fixture)
    :type navigation_response_schema: dict
    """
    navigation_object, response_object = navigation_endpoint_response_down_one
    navigation_json = navigation_object._json
    
    # if the test input data is static (mock data), then `response_object is None`
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(navigation_json, navigation_response_schema)

def test_navigation_two_down_response_validity(
        navigation_endpoint_response_down_two : Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
):
    """
    Validates the JSON response of a remote DTS Navigation endpoint, when retrieving an array
    of all `Citable Unit`s for a given `Resource` down to the second level of the `Resource`'s
    citation tree (`&down=2`). 
    See DTS API specs, section "Navigation Endpoint", example #2.

    :param navigation_endpoint_response_down_two: A tuple containing a `DTS_Navigation` object
        and `requests`' response object.
    :type navigation_endpoint_response_down_two: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: The JSON schema for the DTS Navigation endpoint (Fixture)
    :type navigation_response_schema: Dict
    """
    navigation_object, response_object = navigation_endpoint_response_down_two
    navigation_json = navigation_object._json
    
    # if the test input data is static (mock data), then `response_object is None`
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(navigation_json, navigation_response_schema)

def test_navigation_ref_response_validity(
        navigation_endpoint_response_ref : Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
):
    """Validates the JSON response of a remote DTS Navigation endpoint, when retrieving the entire
    citation subtree for a `Citable Unit` of a given `Resource` (`&down=-1`). 
    See DTS API specs, section "Navigation Endpoint", example #3.

    :param navigation_endpoint_response_ref: A tuple containing a `DTS_Navigation` object
        and `requests`' response object.
    :type navigation_endpoint_response_ref: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: The JSON schema for the DTS Navigation endpoint (Fixture)
    :type navigation_response_schema: Dict
    """
    navigation_object, response_object = navigation_endpoint_response_ref
    navigation_json = navigation_object._json
    
    # if the test input data is static (mock data), then `response_object is None`
    # so we test this assertion only for tests on a remote endpoint
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(navigation_json, navigation_response_schema)

    # the `member` property is expected to contain all citable units 
    # in the citation subtree, thus it can't be empty. This constraint
    # can't be enforced in the Navigation response schema, as there are
    # cases where it may be empty.
    assert navigation_json['member'] is not None

def test_navigation_top_ref_down_two_response_validity(
        navigation_endpoint_response_top_ref_down_two: Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
):
    """Validates the JSON response of a remote DTS Navigation endpoint, when retrieving
    the citation subtree (children + grand-children) for a `Citable Unit` of a given 
    `Resource` (`?ref=<citable_unit)id>&down=2`). 
    See DTS API specs, section "Navigation Endpoint", example #4.

    :param navigation_endpoint_response_top_ref_down_one: A tuple containing a `DTS_Navigation` object
        and `requests`' response object.
    :type navigation_endpoint_response_top_ref_down_one: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: The JSON schema for the DTS Navigation endpoint (Fixture)
    :type navigation_response_schema: Dict
    """
    navigation_object, response_object = navigation_endpoint_response_top_ref_down_two
    navigation_json = navigation_object._json
    
    # if the test input data is static (mock data), then `response_object is None`
    # so we test this assertion only for tests on a remote endpoint
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(navigation_json, navigation_response_schema)

# TODO: finish implementation
def test_navigation_low_ref_down_one_response_validity(
        navigation_endpoint_response_low_ref_down_one : Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
):
    """Validates the JSON response of a remote DTS Navigation endpoint, when retrieving
    the direct children of a low-level `Citable Unit` (= two levels deep) of a given 
    `Resource` (`?ref=<citable_unit)id>&down=1`). 
    See DTS API specs, section "Navigation Endpoint", example #5.

    :param navigation_endpoint_response_low_ref_down_one: A tuple containing a `DTS_Navigation` object
        and `requests`' response object.
    :type navigation_endpoint_response_low_ref_down_one: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: The JSON schema for the DTS Navigation endpoint (Fixture)
    :type navigation_response_schema: Dict
    """
    navigation_object, response_object = navigation_endpoint_response_low_ref_down_one
    navigation_json = navigation_object._json
    
    # if the test input data is static (mock data), then `response_object is None`
    # so we test this assertion only for tests on a remote endpoint
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(navigation_json, navigation_response_schema)

def test_navigation_range_plus_down_response_validity(
        navigation_endpoint_response_range_plus_down : Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
):
    """Validates the JSON response of a remote DTS Navigation endpoint, when retrieving
    an array of `CitableUnit`s in a specified range, including the direct children of the specified
    start and end points (`?start=<citable_unit_1>&end=<citable_unit_2>&down=1`).
    See DTS API specs, section "Navigation Endpoint", example #6.

    :param navigation_endpoint_response_range_plus_down: A tuple containing a `DTS_Navigation` object
        and `requests`' response object.
    :type navigation_endpoint_response_range_plus_down: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: The JSON schema for the DTS Navigation endpoint (Fixture)
    :type navigation_response_schema: Dict
    """
    navigation_object, response_object = navigation_endpoint_response_range_plus_down
    navigation_json = navigation_object._json
    
    # if the test input data is static (mock data), then `response_object is None`
    # so we test this assertion only for tests on a remote endpoint
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(navigation_json, navigation_response_schema)

# TODO: test for invalid combinations of parameters, as per specs
# For each invalid combination, the correspondent HTTP exception should be raised
# `with pytest.raises` is your friend



