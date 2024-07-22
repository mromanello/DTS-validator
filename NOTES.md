# DTS Validator: working notes

## Questions

- Can you confirm that the `page` parameter is *not mandatory* in the URI template for the collection endpoint?
- it's hard to test for e.g. the presence of URI template parameters that are mandatory (or not) depending on the compliance level (see issue #233), if the compliance level of an API implementation is not declared somewhere
    - Shouldn't the compliance level be declared in the Entry endpoint response, similarly to `dtsVersion`?

## Open issues

- is it `Navigation.collection` or `Resource.collection`? [see issue #253](https://github.com/distributed-text-services/specifications/issues/253)
- In the docs, the examples of `Navigation` object are missing the required property  `@type` [see issue #252](https://github.com/distributed-text-services/specifications/issues/252)
    - for now, I've patched the files `tests/data/navigation/*docs*.json`


## Sources of `tests/data/*_docs_*.json`

<details>
<summary>Show table</summary>

| JSON file | DTS specs file| Lines in file |
|-----------|----------------------|---------|
| `entry_docs_response.json` | `specification/versions/unstable/README.md`| 176-186|
| `collection_docs_response_one.json` | `specification/versions/unstable/README.md` | 326-374 |
| `collection_docs_response_readable.json` | `specification/versions/unstable/README.md` | 473-521 |
| `collection_docs_response_root.json` | `specification/versions/unstable/README.md` | 267-313 |
| `navigation_docs_response_down_one.json` | `specification/versions/unstable/README.md` |894-973|
| `navigation_docs_response_down_two.json` | `specification/versions/unstable/README.md` | 993-1126|
| `navigation_docs_response_ref.json` | `specification/versions/unstable/README.md` |1146-1261|
| `navigation_docs_response_down_top_ref_down_two.json` | `specification/versions/unstable/README.md` |1283-1398|
| `navigation/navigation_docs_response_low_ref_down_one.json` | `specification/versions/unstable/README.md` |1418-1498|
| `navigation/navigation_docs_response_range_plus_down.json` | `specification/versions/unstable/README.md` |1519-1680|

</details>

## Validation reports explained

**N.B.:** To better understand what is being tested by each test, it is recommended to read the test's doctsring documentation.

### DraCor DTS API

Entry endpoint: `https://dev.dracor.org/api/v1/dts`

#### Entry endpoint

Full test report: [`dracor_collection_report.html`](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/dracor_entry_report.html)

No failed tests! 🎉

#### Collection endpoint

Full test report: [`dracor_collection_report.html`](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/dracor_collection_report.html)

Explanations about failed tests:
1. `test_collection_endpoint.py::test_readable_collection_response_additional_required_properties`: 
    - Reason: "The required property `collection` (URI template) is missing": this change in the specs (required URI template `collection`) was introduced between version `1-alpha` and `unstable` (the current). 

Other comments:
- The property `totalItems` was deprecated in DTS specs, version `unstable`; only `totalParents` and `totalChildren` are kept. 
- In the `collection` endpoint, the values of the `nav` parameter are not "sanity checked". At the moment, an (invalid) value like `nav=random` does not raise any exception on the API side (I'd expect a `BadRequest`).

#### Navigation endpoint

Full test report: [`dracor_navigation_report.html`](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/dracor_navigation_report.html)

Explanations about failed tests:

1. `tests/test_navigation_endpoint.py::test_navigation_one_down_response_validity`
    - request URI: `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&down=1`
    - Reason: the `Navigation` response object is missing the required `@type` property (to be fully honest, this is missing also in the specs' examples, as per [issue #?]())
    - Comments: in DTS version `unstable` (as opposed to `1-alpha`) the property `passage` was renamed into `document` (see [PR 251](https://github.com/distributed-text-services/specifications/pull/251)).
2. `tests/test_navigation_endpoint.py::test_navigation_two_down_response_validity`
    - request URI: `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&down=2`
    - Reason: the API raises an error here (I understand this wasn't implemented fully yet). The expected behaviour is the following: retrieve a citation sub-tree containing children + grand-children; the corresponding `Citable Unit`s should be contained in the `member` property of the returned `Navigation` response object.
3. `tests/test_navigation_endpoint.py::test_navigation_ref_response_validity`
    - request URI: `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&ref=body&down=-1`
    - Reasons:
        - Same as for test #1: `@type` is missing, and `passage` to be renamed into `document`.
        - `member` property is null, whereas it's expected to contain all `CitableUnit`s in the citation subtree. 
4. `test_navigation_top_ref_down_two_response_validity`
    - request URI: `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&ref=body&down=2`
    - Reason:
        - Same as for test #1: `@type` is missing
5. `test_navigation_range_plus_down_response_validity`
    - request URI: `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&start=front&end=body&down=1`
    - Reason:
        - Same as for test #2 above (caused by `down` not yet fully implemented).
6. simple range test (`start/end`, but no `down`)
    - not yet included in the tests as somehow redundant w.r.t. test #5
    - `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&start=front&end=body&down=1`
    - `member` property is null, whereas it's expected to contain all `CitableUnit`s in the selected citation subtree. 

#### Document endpoint

Full test report: [`dracor_document_report.html`](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/dracor_document_report.html)

No failed tests! 🎉

### FTSR DTS API

Entry endpoint: `http://ftsr-dev.unil.ch:9090/api/dts` (requires VPN)

No failed tests! 🎉 (as of 22.07.2024)