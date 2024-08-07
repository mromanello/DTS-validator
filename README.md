# DTS validator

⚠️ At the moment, this code is VERY work-in-progress!

DTS validator is a suite of tests to validate implementations of the [DTS API](https://w3id.org/dts).  The tests are implemented with `pytest` and the `pytest-html` plugin is used to generate an HTML report of the performed tests. For now, only JSON validation (against JSON schemas) is implemented; JSON-LD validation (against SHACL shapes) will be added later one.

DTS Validator supports version [`unstable`](https://distributed-text-services.github.io/specifications/versions/unstable/) of the specs. 

## Maintenance

- I have derived JSON schemas for all objects defined as per DTS API specs. They schemas can be found in [`schemas/`](./schemas/). If the specs change, the schemas will need to be updated.
- I'm using the JSON examples provided by the specs to run the tests when no remote DTS API is provided. They can be found in `tests/data/`, and are organised by endpoint. JSON object examples that are taken from the docs are contained in files named `*_docs_*.json`. Comments, if present, were stripped from the JSON. 

## Quickstart

```bash

git clone https://github.com/mromanello/DTS-validator.git

cd DTS-validator/

# if you don’t have poetry installed, uncomment the line below
# pip install poetry

poetry install 
poetry shell

make test
```

or you can also run tests for selected endpoints (can be convenient during development):

```bash
make test--entry
make test-collection
make test-navigation
```

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

### Inspecting validation reports

Example of validation reports:
- [all tests on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report.html)
- [tests for `Entry` endpoint on on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report-entry.html)
- [tests for `Collection` endpoint on on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report-collection.html)
- [tests for `Navigation` endpoint on on mock/example data](https://htmlpreview.github.io/?https://github.com/mromanello/DTS-validator/blob/main/reports/report-navigation.html)
- ~~tests for `Document` endpoint on on mock/example data~~

## TODOs

- [ ] tests for DTS Entry endpoint
    - [ ] test semantic of JSON-LD response
- [ ] tests for DTS Collection endpoint
    - [ ] test semantic of JSON-LD response
    - [ ] test pagination if available
- [ ] tests for DTS Navigation endpoint
    - finish test `test_navigation_low_ref_down_one_response_validity` 
- [ ] tests for DTS Document endpoint
    - [ ] test response against schema
    - [ ] test well-formedness of returned XML document/fragment
    - [ ] test (some) requests for different media-types
    - [ ] test for invalid combinations of parameters, as per specs
- [ ] general
    - [ ] support running the validator tests as a package
    - [ ] provide example configuration for integration with CI workflows, e.g. GH Actions



