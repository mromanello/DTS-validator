import logging
import requests
from typing import Dict, Tuple
from dts_validator import DTS_Navigation
from dts_validator.validation import validate_navigation_response

LOGGER = logging.getLogger()

def test_navigation_one_down_response_validity(
        navigation_endpoint_response_down_one : Tuple[DTS_Navigation, requests.models.Response],
        navigation_response_schema: Dict
    ) -> None:
    """
    Validates the JSON response of a remote DTS Navigation endpoint, when retrieving the top-level
    `Citable Unit`s of a given `Resource` (`&down=1`). 

    See specs, section "Navigation Endpoint", example #1.

    :param navigation_endpoint_response_down_one: _description_
    :type navigation_endpoint_response_down_one: Tuple[DTS_Navigation, requests.models.Response]
    :param navigation_response_schema: _description_
    :type navigation_response_schema: _type_
    """
    response_json, response_object = navigation_endpoint_response_down_one
    
    # if the test input data is static (mock data), then `response_object is None`
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(response_json, navigation_response_schema)

def test_navigation_two_down_response_validity(
        navigation_endpoint_response_down_two : Dict,
        navigation_response_schema: Dict
):
    """
    Validates the JSON response of a remote DTS Navigation endpoint, when retrieving an array
    of all `Citable Unit`s for a given `Resource` down to the second level of the `Resource`;s
    citation tree (`&down=2`). 

    See specs, section "Navigation Endpoint", example #1.

    :param navigation_endpoint_response_down_two: _description_
    :type navigation_endpoint_response_down_two: Dict
    :param navigation_response_schema: _description_
    :type navigation_response_schema: Dict
    """
    response_json, response_object = navigation_endpoint_response_down_two
    
    # if the test input data is static (mock data), then `response_object is None`
    if response_object:
        # we expect the endpoint not to raise an exception for this request
        assert response_object.status_code < 400 
    
    # if the request was successful, let's validate the response content
    validate_navigation_response(response_json, navigation_response_schema)

def test_navigation_ref_response_validity(
        navigation_endpoint_response_ref : Dict,
        navigation_response_schema: Dict
):
    """_summary_

    :param navigation_endpoint_response_ref: _description_
    :type navigation_endpoint_response_ref: Dict
    :param navigation_response_schema: _description_
    :type navigation_response_schema: Dict
    """
    validate_navigation_response(navigation_endpoint_response_ref, navigation_response_schema)

def test_navigation_top_ref_down_one_response_validity(
        navigation_endpoint_response_top_ref_down_one : Dict,
        navigation_response_schema: Dict
):
    """_summary_

    :param navigation_endpoint_response_top_ref_down_one: _description_
    :type navigation_endpoint_response_top_ref_down_one: Dict
    :param navigation_response_schema: _description_
    :type navigation_response_schema: Dict
    """
    validate_navigation_response(navigation_endpoint_response_top_ref_down_one, navigation_response_schema)

def test_navigation_low_ref_down_one_response_validity(
        navigation_endpoint_response_low_ref_down_one : Dict,
        navigation_response_schema: Dict
):
    """_summary_

    :param navigation_endpoint_response_low_ref_down_one: _description_
    :type navigation_endpoint_response_low_ref_down_one: Dict
    :param navigation_response_schema: _description_
    :type navigation_response_schema: Dict
    """
    validate_navigation_response(navigation_endpoint_response_low_ref_down_one, navigation_response_schema)

def test_navigation_range_plus_down_response_validity(
        navigation_endpoint_response_range_plus_down : Dict,
        navigation_response_schema: Dict
):
    """_summary_

    :param navigation_endpoint_response_range_plus_down: _description_
    :type navigation_endpoint_response_range_plus_down: Dict
    :param navigation_response_schema: _description_
    :type navigation_response_schema: Dict
    """
    validate_navigation_response(navigation_endpoint_response_range_plus_down, navigation_response_schema)





