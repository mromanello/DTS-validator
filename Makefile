SHELL:=/bin/bash

UBHD_DTS_API?=https://digi.ub.uni-heidelberg.de/editionService/dts/
DRACOR_DTS_API?=https://dev.dracor.org/api/v1/dts
FTSR_DTS_API?=http://ftsr-dev.unil.ch:9090/api/dts/

REPORTS_DIR?=reports
MOCK_REPORTS_DIR=$(REPORTS_DIR)/docs/
UBHD_REPORTS_DIR=$(REPORTS_DIR)/ubhd/
DRACOR_REPORTS_DIR=$(REPORTS_DIR)/dracor/
FTSR_REPORTS_DIR=$(REPORTS_DIR)/ftsr/

##################################################
#    Tests on mock data + examples from docs     #
##################################################

test:
	pytest -s --html=$(MOCK_REPORTS_DIR)/report.html

test-entry:
	pytest tests/test_entry_endpoint.py -s --html=$(MOCK_REPORTS_DIR)/report-entry.html

test-collection:
	pytest tests/test_collection_endpoint.py -s --html=$(MOCK_REPORTS_DIR)/report-collection.html

test-navigation:
	pytest tests/test_navigation_endpoint.py -s --html=$(MOCK_REPORTS_DIR)/report-navigation.html


#####################
#    UNIL FTSR API  #
#####################

test-ftsr-all:
	pytest --entry-endpoint=$(FTSR_DTS_API) -s --html=$(FTSR_REPORTS_DIR)/ftsr_report.html

test-ftsr-entry:
	pytest tests/test_entry_endpoint.py --entry-endpoint=$(FTSR_DTS_API) -s --html=$(FTSR_REPORTS_DIR)/ftsr_entry_report.html

test-ftsr-collection:
	pytest tests/test_collection_endpoint.py --entry-endpoint=$(FTSR_DTS_API) -s --html=$(FTSR_REPORTS_DIR)/ftsr_collection_report.html

test-ftsr-navigation:
	pytest tests/test_navigation_endpoint.py --entry-endpoint=$(FTSR_DTS_API) -s --html=$(FTSR_REPORTS_DIR)/ftsr_entry_report.html

test-ftsr-document:
	pytest tests/test_document_endpoint.py --entry-endpoint=$(FTSR_DTS_API) -s --html=$(FTSR_REPORTS_DIR)/ftsr_document_report.html

#####################
#    DraCor API     #
#####################

test-dracor-all:
	pytest --entry-endpoint=$(DRACOR_DTS_API) -s --html=$(DRACOR_REPORTS_DIR)/dracor_all_report.html

test-dracor-entry:
	pytest tests/test_entry_endpoint.py --entry-endpoint=$(DRACOR_DTS_API) -s --html=$(DRACOR_REPORTS_DIR)/dracor_entry_report.html

test-dracor-collection:
	pytest tests/test_collection_endpoint.py --entry-endpoint=$(DRACOR_DTS_API) -s --html=$(DRACOR_REPORTS_DIR)/dracor_collection_report.html

test-dracor-navigation:
	pytest tests/test_navigation_endpoint.py --entry-endpoint=$(DRACOR_DTS_API) -s --html=$(DRACOR_REPORTS_DIR)/dracor_navigation_report.html

test-dracor-document:
	pytest tests/test_document_endpoint.py --entry-endpoint=$(DRACOR_DTS_API) -s --html=$(DRACOR_REPORTS_DIR)/dracor_document_report.html

test-dracor-strict:
	pytest --entry-endpoint=$(DRACOR_DTS_API) -W error::DeprecationWarning -s --html=$(DRACOR_REPORTS_DIR)/dracor_report.html

#####################
#    UBHD API       #
#####################

test-ubhd-all:
	pytest --entry-endpoint=$(UBHD_DTS_API) -s --html=$(UBHD_REPORTS_DIR)/ubhd_all_report.html

test-ubhd-entry:
	pytest tests/test_entry_endpoint.py --entry-endpoint=$(UBHD_DTS_API) -s --html=$(UBHD_REPORTS_DIR)/ubhd_entry_report.html

test-ubhd-collection:
	pytest tests/test_collection_endpoint.py --entry-endpoint=$(UBHD_DTS_API) -s --html=$(UBHD_REPORTS_DIR)/ubhd_collection_report.html

test-ubhd-navigation:
	pytest tests/test_navigation_endpoint.py --entry-endpoint=$(UBHD_DTS_API) -s --html=$(UBHD_REPORTS_DIR)/ubhd_navigation_report.html

test-ubhd-document:
	pytest tests/test_document_endpoint.py --entry-endpoint=$(UBHD_DTS_API) -s --html=$(UBHD_REPORTS_DIR)/ubhd_document_report.html

test-ubhd-strict:
	pytest --entry-endpoint=$(UBHD_DTS_API) -W error::DeprecationWarning -s --html=$(UBHD_REPORTS_DIR)/ubhd_report.html