# DTS Validator: working notes

## Maintenance

- I have derived JSON schemas for all objects defined as per DTS API specs. They schemas can be found in [`schemas/`](./schemas/). If the specs change, the schemas will need to be updated.
- I'm using the JSON examples provided by the specs to run the tests when no remote DTS API is provided. They can be found in `tests/data/`, and are organised by endpoint. JSON object examples that are taken from the docs are contained in files named `*_docs_*.json`. Comments, if present, were stripped from the JSON. 

## Questions

- Can you confirm that the `page` parameter is *not mandatory* in the URI template for the collection endpoint?
- it's hard to test for e.g. the presence of URI template parameters that are mandatory (or not) depending on the compliance level (see issue #233), if the compliance level of an API implementation is not declared somewhere
    - Shouldn't the compliance level be declared in the Entry endpoint response, similarly to `dtsVersion`?

## Open issues

--


## Sources of `tests/data/*_docs_*.json`

<details>
<summary>Show table</summary>

| JSON file | DTS specs file| Lines in file |
|-----------|----------------------|---------|
| `entry_docs_response.json` | `specification/versions/unstable/README.md`| 184-192|
| `collection_docs_response_one.json` | `specification/versions/unstable/README.md` | 350-396 |
| `collection_docs_response_readable.json` | `specification/versions/unstable/README.md` | 473-521 |
| `collection_docs_response_root.json` | `specification/versions/unstable/README.md` | 267-313 |
| `navigation_docs_response_down_one.json` | `specification/versions/unstable/README.md` |894-973|
| `navigation_docs_response_down_two.json` | `specification/versions/unstable/README.md` | 1034-1166|
| `navigation_docs_response_ref.json` | `specification/versions/unstable/README.md` |1146-1261|
| `navigation_docs_response_down_top_ref_down_two.json` | `specification/versions/unstable/README.md` |1283-1398|
| `navigation/navigation_docs_response_low_ref_down_one.json` | `specification/versions/unstable/README.md` |1418-1498|
| `navigation/navigation_docs_response_range_plus_down.json` | `specification/versions/unstable/README.md` |1519-1680|

</details>