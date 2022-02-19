.PHONY: prepare run test

.EXPORT_ALL_VARIABLES:
PYTHONPATH = $PYTHONPATH:${pwd}
VENV_DIR ?= venv

prepare:
	python3.8 -m venv venv;
	. ${VENV_DIR}/bin/activate;
	pip install -r requirements.txt;

run:
	. ${VENV_DIR}/bin/activate;
	python3.8 run.py;

test:
	. ${VENV_DIR}/bin/activate;
	export ENV="test";
	python -m unittest discover -v -s test -p *_test.py;