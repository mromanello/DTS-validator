import logging
import requests
from requests.models import Response
from typing import Optional, Union, List
from uritemplate import URITemplate

LOGGER = logging.getLogger()

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

class DTS_CitableUnit(object):
    def __init__(self, raw_json) -> None:
        self._json = raw_json
        self.id = raw_json["identifier"]
        self.level = int(raw_json["level"])
        self.type = raw_json["citeType"]

    def __repr__(self) -> str:
        return f'DTS_CitableUnit(id={self.id}, type={self.type}, level={self.level})'

class DTS_CitationMap(object):
    def __init__(self, raw_json) -> None:
        self._json = raw_json
        self.citable_units = []
        if 'member' in self._json: 
            for unit in self._json['member']:
                self.citable_units.append(DTS_CitableUnit(unit))

# when this in instantiated (visiting the Collection endpoint)
# its citationTrees need to be instantiated already
class DTS_Resource(DTS_Collection):
    def __init__(self, raw_json):
        super().__init__(raw_json)

    def __repr__(self) -> str:
        return f'DTS_Resource(id={self.id})'

# TODO: find a cleaner way of triggering the header validation
class DTS_API(object):
    def __init__(self, entry_endpoint_uri) -> None:
        req  = requests.get(entry_endpoint_uri)
        assert 'application/ld+json' in req.headers['Content-Type'] # TODO: wrap around a try/except statement
        self._entry_endpoint_json = req.json()

        # initialise URI templates
        self._collection_endpoint_template = URITemplate(self._entry_endpoint_json['collection'])
        self._document_endpoint_template = URITemplate(self._entry_endpoint_json['document'])
        self._navigation_endpoint_template = URITemplate(self._entry_endpoint_json['navigation'])

        # TODO pagination can be supported in collection or navigation endpoints => check that

    def collections(
            self, id: Optional[str] = None,
            recursive: bool = False,
            navigation: str = 'children'
        ) -> Union[List[DTS_Collection], DTS_Collection]:
        # get the root of the collection endpoint
        if id is None:
            if navigation == 'parents':
                collection_req_uri = self._collection_endpoint_template.expand({'nav': navigation})
            else:
                collection_req_uri = self._collection_endpoint_template.expand() # leave the default value of `nav` implicit
            
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
            if navigation == 'parents':
                collection_req_uri = self._collection_endpoint_template.expand({'id': id, 'nav': navigation})
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
            else:
                return None
    
    def navigate(
            self,
            resource: DTS_Resource,
            down: int = None,
            reference: str = None,
            start: str = None,
            end: str = None
    ) -> Response:
        parameters = {
            "resource": resource.id,
            "down": down,
            "ref": reference,
            "start": start,
            "end": end
        }
        navigation_endpoint_template = URITemplate(resource._json['navigation'])
        navigation_endpoint_uri = navigation_endpoint_template.expand(parameters)
        request = requests.get(navigation_endpoint_uri)
        return request

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