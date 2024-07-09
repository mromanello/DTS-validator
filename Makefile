SHELL:=/bin/bash

REPORTS_DIR?=reports

test:
	pytest -s --html=$(REPORTS_DIR)/report.html

test-ftsr:
	pytest --entry-endpoint=http://ftsr-dev.unil.ch:9090/dts/api/v1/ -s --html=$(REPORTS_DIR)/ftsr_unil_report.html

test-dracor:
	pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts -s --html=$(REPORTS_DIR)/dracor_report.html

test-dracor-strict:
	pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts -W error::DeprecationWarning -s --html=$(REPORTS_DIR)/dracor_report.html

