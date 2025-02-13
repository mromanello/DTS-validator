from __future__ import annotations
import logging
import requests
import random
from requests.models import Response
from typing import Optional, Union, List, Tuple, Dict
from uritemplate import URITemplate
from .validation import check_required_property


LOGGER = logging.getLogger()

class DTS_Collection(object):
    """Class representing a DTS Collection object."""
    
    def __init__(self, raw_json) -> None:
        self._json = raw_json
        self.id = raw_json["@id"]

    @property
    def json(self):
        return self._json

    @property
    def children(self) -> List[DTS_Collection]:
        """Returns the collections contained in the current collection. 

        :return: The list of nested collections.
        :rtype: List[DTS_Collection]
        """
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

# when this in instantiated (visiting the Collection endpoint)
# its citationTrees need to be instantiated already
class DTS_Resource(DTS_Collection):
    """Class representing a DTS Resource object (a.k.a. document or readable collection)."""

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def __repr__(self) -> str:
        return f'DTS_Resource(id={self.id})'

class DTS_CitableUnit(object):
    """Class representing a DTS CitableUnit object.
    As per the DTS documentation, a `CitableUnit` is a portion of a `Resource` identified by a reference string."""
    def __init__(self, raw_json) -> None:
        self._json = raw_json
        self.id = raw_json["identifier"]
        self.level = int(raw_json["level"])
        self.type = raw_json["citeType"]
        self.parent = raw_json["parent"] if "parent" in raw_json else None

    def __repr__(self) -> str:
        return f'DTS_CitableUnit(id={self.id}, type={self.type}, level={self.level})'

class DTS_Navigation(object):
    def __init__(self, raw_json) -> None:
        self._json = raw_json
        self.id = raw_json["@id"]
        self.citable_units = []
        self.reference = None
        self.start = None
        self.end = None
        self.resource = DTS_Resource(self._json['resource'])

        # populate additional properties from a DTS Navigation endpoint response JSON
        if 'member' in self._json and self._json['member']: 
            for unit in self._json['member']:
                self.citable_units.append(DTS_CitableUnit(unit))

        if 'ref' in self._json and self._json['ref']:
            self.reference = DTS_CitableUnit(self._json['ref'])

        if 'start' in self._json and self._json['start']:
            self.start = DTS_CitableUnit(self._json['start'])

        if 'end' in self._json and self._json['end']:
            self.end = DTS_CitableUnit(self._json['end'])

    def __repr__(self) -> str:
        return f'DTS_navigation(id={self.id})'

# TODO: find a cleaner way of triggering the header validation
class DTS_API(object):
    def __init__(self, entry_endpoint_uri) -> None:
        req  = requests.get(entry_endpoint_uri)
        assert 'application/ld+json' in req.headers['Content-Type'] # TODO: wrap around a try/except statement
        self._entry_endpoint_json = req.json()

        # before using the URI templates, let's make sure that they are 
        # declared by the Entry endpoint as expected
        check_required_property(self._entry_endpoint_json, 'collection')
        check_required_property(self._entry_endpoint_json, 'document')
        check_required_property(self._entry_endpoint_json, 'navigation')

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
            
            LOGGER.info(f'URI of request to Collection endpoint: {collection_req_uri}')
            collection_req = requests.get(collection_req_uri)
            collection_req.raise_for_status()
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
            LOGGER.info(f'URI of request to Collection endpoint: {collection_req_uri}')
            collection_req = requests.get(collection_req_uri)
            collection_req.raise_for_status()
            return DTS_Collection(collection_req.json())
    
    def get_one_resource(self):
        collections = self.collections()
        random.shuffle(collections)
        for collection in collections:
            resource  = get_resource_recursively(collection, self)
            if resource:
                return resource
            else:
                return None
    
    def navigation(
            self,
            resource: DTS_Resource,
            down: int = None,
            reference: DTS_CitableUnit = None,
            start: DTS_CitableUnit = None,
            end: DTS_CitableUnit = None
    ) -> Tuple[DTS_Navigation, Response]:
        """_summary_

        :param resource: _description_
        :type resource: DTS_Resource
        :param down: _description_, defaults to None
        :type down: int, optional
        :param reference: _description_, defaults to None
        :type reference: DTS_CitableUnit, optional
        :param start: _description_, defaults to None
        :type start: DTS_CitableUnit, optional
        :param end: _description_, defaults to None
        :type end: DTS_CitableUnit, optional
        :return: _description_
        :rtype: Tuple[DTS_Navigation, Response]
        """
        parameters = {
            "resource": resource.id,
            "down": down,
            "ref": reference.id if reference else None,
            "start": start.id if start else None,
            "end": end.id if end else None
        }
        navigation_endpoint_template = URITemplate(resource._json['navigation'])
        navigation_endpoint_uri = navigation_endpoint_template.expand(parameters)
        LOGGER.info(f'URI of request to Navigation endpoint: {navigation_endpoint_uri}')
        response = requests.get(navigation_endpoint_uri)
        if response.status_code == 200:
            return (DTS_Navigation(response.json()), response)
        else:
            return (None, response)

    def document(
            self,
            resource: DTS_Resource,
            reference: DTS_CitableUnit = None,
            start: DTS_CitableUnit = None,
            end: DTS_CitableUnit = None
    ) -> Tuple[str, Response]:
        """navigation_or_collection

        :param resource: _description_
        :type resource: DTS_Resource
        :param reference: _description_, defaults to None
        :type reference: DTS_CitableUnit, optional
        :param start: _description_, defaults to None
        :type start: DTS_CitableUnit, optional
        :param end: _description_, defaults to None
        :type end: DTS_CitableUnit, optional
        :return: _description_
        :rtype: Tuple[str, Response]
        """
        # get IDs from the input objects, and use them as values for URI parameters
        parameters = {
            "resource": resource.id,
            "ref": reference.id if reference else None,
            "start": start.id if start else None,
            "end": end.id if end else None
        }
        if 'document' in resource.json:
            document_endpoint_template = URITemplate(resource.json['document'])
        else:
            raise ValueError("Missing document URI-Template")

        document_endpoint_uri = document_endpoint_template.expand(parameters)
        LOGGER.info(f'URI of request to Document endpoint: {document_endpoint_uri}')
        response = requests.get(document_endpoint_uri)
        if response.status_code == 200:
            return (response.content.decode(), response)
        else:
            return (None, response)

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