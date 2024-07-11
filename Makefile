SHELL:=/bin/bash

REPORTS_DIR?=reports

##################################################
#    Tests on mock data + examples from docs     #
##################################################

test:
	pytest -s --html=$(REPORTS_DIR)/report.html

test-entry:
	pytest tests/test_entry_endpoint.py -s --html=$(REPORTS_DIR)/report-entry.html

test-collection:
	pytest tests/test_collection_endpoint.py -s --html=$(REPORTS_DIR)/report-collection.html

test-navigation:
	pytest tests/test_navigation_endpoint.py -s --html=$(REPORTS_DIR)/report-navigation.html


#####################
#    UNIL FTSR API  #
#####################

test-ftsr-all:
	pytest --entry-endpoint=http://ftsr-dev.unil.ch:9090/dts/api/v1/ -s --html=$(REPORTS_DIR)/ftsr_unil_report.html

#####################
#    DraCor API     #
#####################

test-dracor-all:
	pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts -s --html=$(REPORTS_DIR)/dracor_all_report.html

test-dracor-entry:
	pytest tests/test_entry_endpoint.py --entry-endpoint=https://dev.dracor.org/api/v1/dts -s --html=$(REPORTS_DIR)/dracor_entry_report.html

test-dracor-collection:
	pytest tests/test_collection_endpoint.py --entry-endpoint=https://dev.dracor.org/api/v1/dts -s --html=$(REPORTS_DIR)/dracor_collection_report.html

test-dracor-navigation:
	pytest tests/test_navigation_endpoint.py --entry-endpoint=https://dev.dracor.org/api/v1/dts -s --html=$(REPORTS_DIR)/dracor_navigation_report.html

test-dracor-strict:
	pytest --entry-endpoint=https://dev.dracor.org/api/v1/dts -W error::DeprecationWarning -s --html=$(REPORTS_DIR)/dracor_report.html

