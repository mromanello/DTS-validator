import logging
import requests
from typing import Dict, Tuple, Optional
from dts_validator.client import DTS_Navigation

LOGGER = logging.getLogger(__name__)

# Cases to test:
# resource_id + down
# resource_id + ref
# resource_id + start/end

def test_document_ref_response_validity(document_endpoint_response_ref):
    pass
