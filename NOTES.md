## Questions

- Can you confirm that the `page` parameter is *not mandatory* in the URI template for the collection endpoint?
- it's hard to test for e.g. the presence of URI template parameters that are mandatory (or not) depending on the compliance level (see issue #233), if the compliance level of an API implementation is not declared somewhere
    - Shouldn't the compliance level be declared in the Entry endpoint response, similarly to `dtsVersion`?

## Issues

- is it `Navigation.collection` or `Resource.collection`? [see issue #253](https://github.com/distributed-text-services/specifications/issues/253)
- In the docs, the examples of `Navigation` object are missing the required property  `@type` [see issue #252](https://github.com/distributed-text-services/specifications/issues/252)
    - for now, I've patched the files `tests/data/navigation/*docs*.json`

## Comments about implementations

### DraCor


#### Entry endpoint

Full test report: [`dracor_collection_report.html`](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/dracor_entry_report.html)

No failed tests! 🎉

#### Collection endpoint

Full test report: [`dracor_collection_report.html`](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/dracor_collection_report.html)

Failed tests (n=1):
- test `test_collection_endpoint.py::test_readable_collection_response_additional_required_properties`: 
    - Reason: "The required property `collection` (URI template) is missing": this change in the specs (required URI template `collection`) was introduced between version `1-alpha` and `unstable` (the current). 

Comments:
- In the `collection` endpoint, the values of the `nav` parameter are not "sanity checked". At the moment, an (invalid) value like `nav=random` does not raise any exception on the API side (I'd expect a `BadRequest`).

#### Navigation endpoint

(add references to the tests that fail)

- `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&down=1`
    - the Navigation response object is missing the required `@type` property
- the `passage` property will be renamed to `document` (see [issue 249](https://github.com/distributed-text-services/specifications/issues/249))
- `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&down=2`
    - I'd expect a different behaviour
- `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&ref=body&down=-1`
    - here the `member` property is null, whereas it's expected to contain all `CitableUnit`s in the selected citation subtree. 
- when retrieving a range (start/end), the CitableUnits in the range must be included in the `member` property

### FTSR