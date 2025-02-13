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
    - [x] support running the validator tests as a package
    - [x] provide example configuration for integration with CI workflows, e.g. GH Actions