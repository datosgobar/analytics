NOTEBOOKS ?=./notebooks/*.ipynb
NOTEBOOK ?=./notebooks/georef_analytics.ipynb
REPORT ?=./reports/georef_analytics.html

georef_report: NOTEBOOK =./notebooks/georef_analytics.ipynb
georef_report: REPORT =./reports/georef_analytics.html

all: pull reports commit push

pull:
	git -C .. pull

reports: georef_report

georef_report: update_analytics
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1 --to notebook --inplace --output-dir ./reports $(NOTEBOOK)
	jupyter nbconvert  --no-input --to html --output-dir ./reports $(NOTEBOOK)
	$(MAKE) clean_white_spaces REPORT=$(REPORT)

clean_white_spaces:
	python shrink_file.py --file '$(REPORT)'

commit:
	git -C .. commit -a

push:
	git -C .. push

update_analytics:
	python3 ../tools/analytics_tools.py
# html:
# 	jupyter nbconvert  --template data-report.tpl --to html --output-dir ./reports $(NOTEBOOKS)
