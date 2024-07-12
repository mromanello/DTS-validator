# DTS validator

⚠️ At the moment, this code is VERY work-in-progress!

DTS validator is a suite of tests to validate implementations of the [DTS API](https://w3id.org/dts). Its current support is limited to version `1-alpha` of the specs. The tests are implemented with `pytest` and the `pytest-html` plugin is used to generate an HTML report of the performed tests. 

## Design

- I decided to focus on JSON validation (against JSON schemas) for now and leave for later JSON-LD validation (against SHACL shapes). 

## Maintenance

- I have derived JSON schemas for all objects defined as per DTS API specs. They schemas can be found in [`schemas/`](./schemas/). If the specs change, the schemas will need to be updated.
- I'm using the JSON examples provided by the specs to run the tests when no remote DTS API is provided. They can be found in `tests/data/`, and are organised by endpoint. JSON object examples that are taken from the docs are contained in files named `*_docs_*.json`. Comments, if present, were stripped from the JSON. 

## Usage
### How to run the validator

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

For more examples, see the commands contained in the [`Makefile`](./Makefile).

### Validation reports

Example of validation reports:
- [all tests on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report.html)
- [tests for `Entry` endpoint on on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report-entry.html)
- [tests for `Collection` endpoint on on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report-collection.html)
- [tests for `Navigation` endpoint on on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report-navigation.html)
- ~~tests for `Document` endpoint on on mock/example data~~

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
- [x] tests for DTS Navigation endpoint
    - [x] test response against schema
- [ ] tests for DTS Document endpoint
    - [ ] test response against schema
    - [ ] test well-formedness of returned XML document/fragment
    - [ ] test (some) requests for different media-types
- [ ] provide example configuration for integration with CI workflows, e.g. GH Actions
