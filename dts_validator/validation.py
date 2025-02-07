import logging
import warnings
import pathlib
import os.path
from jsonschema.exceptions import ValidationError, SchemaError
from jsonschema import validate, RefResolver
from uritemplate import URITemplate
from .exceptions import URITemplateMissingParameter, JSONResponseMissingProperty

LOGGER = logging.getLogger()



def validate_json(json_data, json_schema):
    # Set up resolver to correctly handle relative paths
    resolver = RefResolver(
        base_uri=(pathlib.Path(__file__) / ".." / ".." / "schemas").resolve().as_uri() + "/",
        referrer=json_schema
    )
    try:
        assert validate(json_data, json_schema, resolver=resolver) is None
        LOGGER.info('JSON schema and JSON response are valid.')
    except SchemaError as e:
         LOGGER.error(f'The provided JSON schema is invalid according to its metaschema.')
    except ValidationError as e:
        LOGGER.error(f'The JSON response is invalid according to the provided schema.')
        raise e
    return None

def validate_uri_template(uri_template, template_name, required_parameters) -> None:
    
    uri_template = URITemplate(uri_template)
    available_parameters = list(uri_template.variable_names)
    
    for param in required_parameters:
            try:
                assert param in available_parameters
                msg = f'Expected parameter `{param}` is contained in the `{template_name}` URI template {uri_template}'
                LOGGER.info(msg)
            except AssertionError:
                msg = f'Parameter `{param}` must be contained in the `{template_name}` URI template {uri_template} (available parameters: {available_parameters})'
                LOGGER.error(msg)
                raise URITemplateMissingParameter(msg)

# TODO: check if the property value is valid (against a list of valid values)
def check_required_property(json_data, property_name):
    try:
        assert property_name in json_data
        LOGGER.info(f'The property `{property_name}` is present as expected')
    except AssertionError as e:
        LOGGER.error(f'The required property `{property_name}` (URI template) is missing in the following JSON: {json_data}')
        raise JSONResponseMissingProperty(f'The required property `{property_name}` (URI template) is missing')

def check_deprecated_property(json_data, property_name):
    try:
        assert property_name not in json_data
    except AssertionError as e:
        warn_message = f'The property `{property_name}` is present in the JSON but it was deprecated'
        warnings.warn(warn_message, category=DeprecationWarning)

def validate_collection_response(json_data, json_schema):
    validate_json(json_data, json_schema)
    check_deprecated_property(json_data, 'totalItems')
    check_required_property(json_data, 'dtsVersion')

# TODO: implement
def validate_navigation_response(json_data, json_schema):
    validate_json(json_data, json_schema)
    # TODO: finish...