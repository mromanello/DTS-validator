## Questions

- Can you confirm that the `page` parameter is *not mandatory* in the URI template for the collection endpoint?
- it's hard to test for e.g. the presence of URI template parameters that are mandatory (or not) depending on the compliance level (see issue #233), if the compliance level of an API implementation is not declared somewhere
    - Shouldn't the compliance level be declared in the Entry endpoint response, similarly to `dtsVersion`?

## Comments about implementations

### DraCor

#### Collection endpoint

- in the `collection` endpoint, validate the values of the `nav` parameter. At the moment, an invalid value like `nav=random` does not raise any exception on the API side (I'd expect a `BadRequest`).

#### Navigation endpoint

- `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&down=1`
    - the Navigation response object is missing the required `@type` property
- the `passage` property will be renamed to `document` (see [issue 249](https://github.com/distributed-text-services/specifications/issues/249))
- `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&down=2`
    - I'd expect a different behaviour
- `https://dev.dracor.org/api/v1/dts/navigation?resource=https://dev.dracor.org/id/test000001&ref=body&down=-1`
    - here `member` property is null
- when retrieving a range (start/end), the CitableUnits in the range are included in `member`

### FTSR