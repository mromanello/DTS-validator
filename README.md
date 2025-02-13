# DTS validator

[![Test validation](https://github.com/mromanello/DTS-validator/actions/workflows/main.yml/badge.svg)](https://github.com/mromanello/DTS-validator/actions/workflows/main.yml)

DTS validator is a suite of tests to validate implementations of the [DTS API](https://w3id.org/dts).  The tests are implemented with `pytest` and the `pytest-html` plugin is used to generate an HTML report of the performed tests. For now, only JSON validation (against JSON schemas) is implemented; JSON-LD validation (against SHACL shapes) will be added later on.

**NB:** DTS Validator supports version [`unstable`](https://distributed-text-services.github.io/specifications/versions/unstable/) of the specs; it is currently up-to-date with commit [ef8c7cdaf789b61a1b7949fe42b1f168982a102a](https://github.com/distributed-text-services/specifications/commit/ef8c7cdaf789b61a1b7949fe42b1f168982a102a) of the DTS specs repo.

## Installation

### With `pip`

```bash
pip install https://github.com/mromanello/DTS-validator/archive/refs/heads/main.zip

# to check that everything works
dts-validator --help

# to run the default tests
dts-validator --html=dts_validation_report.html
```

### By cloning the repo

<details>
<summary>Show more</summary>

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

</details>

## Usage

### How to run the validator
<details>
<summary>Show more</summary>

Use the `--entry-endpoint` parameter to provide the URI of the API to be validated:

```bash
dts-validator --entry-endpoint=https://dev.dracor.org/api/v1/dts
```

Additionally, an HTML test report can be output; just provide the path of the HTML file:

```bash
dts-validator --entry-endpoint=https://dev.dracor.org/api/v1/dts --html=report.html
```

For a more verbose report, change the `--log-level` to `DEBUG`:

```bash
dts-validator --entry-endpoint=https://dev.dracor.org/api/v1/dts --html=report.html --log-cli-level=debug
```

If no `--entry-endpoint` is provided, a series of mock tests will be executed:

```bash
dts-validator --html=report.html
```

For more examples, see the commands contained in the [`Makefile`](./Makefile).

</details>

## Validation of known implementations

| Name | API entry endpoint | DTS version |Validation status |
|-------|-----|-------------|-------------------|
| DraCor | https://dev.dracor.org/api/v1/dts | `unstable`|[![Validate DraCor (dev) API](https://github.com/mromanello/DTS-validator/actions/workflows/dracor.yml/badge.svg)](https://github.com/mromanello/DTS-validator/actions/workflows/dracor.yml) |
| UBHD | https://digi.ub.uni-heidelberg.de/editionService/dts/ | `unstable`|[![Validate UBHD API](https://github.com/mromanello/DTS-validator/actions/workflows/ubhd.yml/badge.svg)](https://github.com/mromanello/DTS-validator/actions/workflows/ubhd.yml) |
