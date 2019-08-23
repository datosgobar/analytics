NOTEBOOKS ?='./notebooks/*.ipynb'
NOTEBOOK ?=./notebooks/ips-historicos.ipynb
REPORT ?=./reports/ips-historicos.html

ips_report: NOTEBOOK =./notebooks/ips-historicos.ipynb
ips_report: REPORT =./reports/ips-historicos.html

all: pull reports commit push

pull:
	git -C .. pull

reports: ips_report

update_analytics:
	python3 ../tools/analytics_tools.py

ips_report: update_analytics
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1 --to notebook --inplace --output-dir ./reports $(NOTEBOOK)
	jupyter nbconvert  --to html --output-dir ./reports $(NOTEBOOK)
	$(MAKE) clean_white_spaces REPORT=$(REPORT)

clean_white_spaces:
	python shrink_file.py --file '$(REPORT)'

commit:
	git -C .. commit -a

push:
	git -C .. push

# html:
# 	jupyter nbconvert  --template data-report.tpl --to html --output-dir ./reports $(NOTEBOOKS)
