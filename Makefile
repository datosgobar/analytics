VIRTUALENV = analytics
ANALYTICS_PIP ?= pip3
ANALYTICS_PYTHON ?= python3

DATE = date +%y-%m-%dT%H:%M:%S

install_anaconda:
	wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
	bash Miniconda3-latest-Linux-x86_64.sh
	rm Miniconda3-latest-Linux-x86_64.sh
	export PATH=$$PATH:/home/series/miniconda3/bin

setup_anaconda:
	conda create -n $(CONDA_ENV) --no-default-packages
	source activate $(CONDA_ENV); \
		$(ANALYTICS_PIP) install -r requirements.txt

setup_virtualenv:
	test -d $(VIRTUALENV)/bin/activate || $(ANALYTICS_PYTHON) -m venv $(VIRTUALENV)
	source $(VIRTUALENV)/bin/activate; \
		$(ANALYTICS_PIP) install -r requirements.txt

all_reports: pull reports commit push
reports: reports_api_gateway reports_georef reports_series_tiempo

reports_api_gateway:
	cd api-gateway; $(MAKE) reports

reports_georef:
	cd georef-ar-api; $(MAKE) reports

reports_series_tiempo:
	cd series-tiempo-ar-api; $(MAKE) reports

pull:
	git pull

commit:
	git commit -a

push:
	git push

update_analytics:
	python3 ./tools/analytics_tools.py
