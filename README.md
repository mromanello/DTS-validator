# DTS validator

⚠️ At the moment, this code is VERY work-in-progress!

DTS validator is a suite of tests to validate implementations of the [DTS API](https://w3id.org/dts). Its current support is limited to version `1-alpha` of the specs. The tests are implemented with `pytest` and the `pytest-html` plugin is used to generate an HTML report of the performed tests. 

## Design

TBD

## Manteinance

TBD

## How to run the validator

Use the `--entry-endpoint` parameter to provide the URI of the API to be validated:

```bash
pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts
```

Additionally, an HTML test report can be output; just provide the path of the HTML file:

```bash
pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts --html=report.html
```

For a more verbose report, change the `--log-level` to `DEBUG`:

```bash
pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts --html=report.html --log-cli-level=debug
```

If no `--entry-endpoint` is provided, a series of mock tests will be executed:

```bash
pytest --html=report.html
```

## TODOs

- [ ] tests for DTS Entry endpoint
    - [x] check response headers (Content-Type)
    - [x] test response against schema
    - [x] check URI templates 
    - [ ] test semantic of JSON-LD response
- [ ] tests for DTS Collection endpoint
    - [ ] check response headers (Content-Type)
    - [x] update the Collection response schema (copied the old one by @monotasker)
    - [x] add a warning if `totalItems` is still present (it was removed as per this [PR](https://github.com/distributed-text-services/specifications/pull/251#event-12925576483))
    - [x] test response against schema
    - [x] check URI templates (especially when collection is readable)
- [ ] tests for DTS Navigation endpoint
    - [ ] test response against schema
- [ ] tests for DTS Document endpoint
    - [ ] test response against schema
    - [ ] test well-formedness of returned XML document/fragment
    - [ ] test (some) requests for different media-types
- [ ] provide example configuration for integration with CI workflows, e.g. GH Actions

## Notes

```python
warnings.warn('hey user', category=DeprecationWarning)

client = DTS_API('https://dev.dracor.org/api/v1/dts')
client._entry_endpoint_json 
client.collections()
client.media_types -> returns a list (strings) of the supported media types
client._collection_endpoint_json
client.collections(readable=True) -> returns DTS_Resource (subclass of DTS_Collection)
client.collections(id=collection_id) -> returns DTS_Collection
client.navigate(resource_id) -> returns a list of DTS_CitableUnit
client.document(resource_id, ref=..., media_type=...)
```
