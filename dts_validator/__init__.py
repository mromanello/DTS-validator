import logging
import requests
from uritemplate import URITemplate
from jsonschema import validate
from jsonschema.exceptions import ValidationError

LOGGER = logging.getLogger()

def validate_json(json_data, json_schema):
    LOGGER.info(json_data)
    try:
        assert validate(json_data, json_schema) is None
        LOGGER.info('JSON schema and JSON response are valid.')
    except ValidationError as e:
        # TODO catpure more specific exceptions from `jsonschema.validate()`
        LOGGER.error('Either the JSON schema or the JSON object are invalid.')
        raise e
    return None



class DTS_Collection(object):
    def __init__(self, raw_json) -> None:
        self._json = raw_json
        self.id = raw_json["@id"]

    @property
    def children(self):
        children = []
        if 'member' in self._json: 
            for member in self._json['member']:
                if member['@type'] == "Resource":
                    children.append(DTS_Resource(member))
                else:
                    children.append(DTS_Collection(member))
        return children

    def __repr__(self) -> str:
        return f'DTS_Collection(id={self.id})'
    

class DTS_Resource(DTS_Collection):
    def __init__(self, raw_json):
        super().__init__(raw_json)

    def __repr__(self) -> str:
        return f'DTS_Resource(id={self.id})'


class DTS_API(object):
    def __init__(self, entry_endpoint_uri) -> None:
        req  = requests.get(entry_endpoint_uri)
        assert 'application/ld+json' in req.headers['Content-Type'] # TODO: wrap around a try/except statement
        self._entry_endpoint_json = req.json()

        # initialise URI templates
        self._collection_endpoint_template = URITemplate(self._entry_endpoint_json['collection'])
        self._document_endpoint_template = URITemplate(self._entry_endpoint_json['document'])
        self._navigation_endpoint_template = URITemplate(self._entry_endpoint_json['navigation'])

    def collections(self, id=None, recursive=False):
        # get the root of the collection endpoint
        if id is None:
            collection_req_uri = self._collection_endpoint_template.expand()
            collection_req = requests.get(collection_req_uri)
            self._collection_endpoint_json = collection_req.json()
            try:
                assert 'application/ld+json' in collection_req.headers['Content-Type']
            except AssertionError:
                msg = f"Missing 'application/ld+json' in Content-Type header"
                LOGGER.error(msg)

            # get all collection IDs
            if 'member' in self._collection_endpoint_json:
                if recursive:
                    collections = [
                        get_collections_recursively(DTS_Collection(member), self)
                        for member in self._collection_endpoint_json['member']
                    ]
                else:
                    collections = [DTS_Collection(member) for member in self._collection_endpoint_json['member']]
                return collections
            else:
                return []
        # get a specific collection, by ID
        else:
            collection_req_uri = self._collection_endpoint_template.expand({'id': id})
            collection_req = requests.get(collection_req_uri)
            return DTS_Collection(collection_req.json())
    
    def get_one_resource(self):
        collections = self.collections()
        for collection in collections:
            resource  = get_resource_recursively(collection, self)
            if resource:
                return resource
            

def get_resource_recursively(collection : DTS_Collection, dts_client : DTS_API) -> DTS_Resource:
    # get the full metadata from the API    
    collection = dts_client.collections(id=collection.id)
    
    if isinstance(collection, DTS_Resource):
        return collection
    else:
        for child in collection.children:
            if isinstance(child, DTS_Resource):
                resource = child
                continue
            else:
                return get_resource_recursively(child, dts_client)
        return resource
    
# TODO: rewrite using new objects
def get_collections_recursively(collection, dts_client):
    print(f'processing recursively collection {collection.id}')
    collection = dts_client.collections(id=collection.id)
    if 'member' in collection._json:
        return [
            get_collections_recursively(DTS_Collection(member), dts_client)
            for member in collection._json['member']
        ]
    else:
        return collection