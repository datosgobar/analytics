NOTEBOOKS ?=./notebooks/*.ipynb
NOTEBOOK ?=./notebooks/series-informe-bcra.ipynb
REPORT ?=./reports/series-informe-bcra.html

sspm_report: NOTEBOOK =./notebooks/series-informe-sspm.ipynb
sspm_report: REPORT =./reports/series-informe-sspm.html
bcra_report: NOTEBOOK =./notebooks/series-informe-bcra.ipynb
bcra_report: REPORT =./reports/series-informe-bcra.html
all_report: NOTEBOOK =./notebooks/series-informe-total.ipynb
all_report: REPORT =./reports/series-informe-total.html

all: pull reports commit push

pull:
	git -C .. pull

reports: all_report sspm_report bcra_report

sspm_report: update_analytics
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1 --to notebook --inplace --output-dir ./reports $(NOTEBOOK)
	jupyter nbconvert --to html --output-dir ./reports $(NOTEBOOK)
	$(MAKE) clean_white_spaces REPORT=$(REPORT)

bcra_report: update_analytics
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1 --to notebook --inplace --output-dir ./reports $(NOTEBOOK)
	jupyter nbconvert --to html --output-dir ./reports $(NOTEBOOK)
	$(MAKE) clean_white_spaces REPORT=$(REPORT)

all_report: update_analytics
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1 --to notebook --inplace --output-dir ./reports $(NOTEBOOK)
	jupyter nbconvert --to html --output-dir ./reports $(NOTEBOOK)
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

# watch:
# 	while inotifywait -e close_write $(NOTEBOOK); do jupyter nbconvert  --template data-report.tpl --to html --output-dir ./reports $(NOTEBOOK); done
