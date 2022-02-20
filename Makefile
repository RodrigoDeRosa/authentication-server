.PHONY: prepare run test

.EXPORT_ALL_VARIABLES:
PYTHONPATH = $PYTHONPATH:${pwd}
VENV_DIR ?= venv

run:
	docker-compose up --build -d postgres app

test:
	. ${VENV_DIR}/bin/activate;
	export ENV="test";
	python3 -m unittest discover -v -s test -p *_test.py;