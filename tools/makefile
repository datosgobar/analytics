API?=series-tiempo-prod
END_DATE?= `date '+%Y-%m-%d'`
OUTPUT_DIR_SDT?=~/sdt-analytics-download
OUTPUT_DIR_GR?=~/gr-analytics-download
COOKIE?='_ga=GA1.3.2107340663.1525456734; _gid=GA1.3.1307509621.1557233941; mgmtsessionid=i9b6d236kce40k26y864j20bqcti46pa; csrftoken=2lZgjMtLsI0LWtuc3DIZru1zwn2rirapPtWPh3BsDftfdWOJnUP3eZ0Y2NtujyeE'

FROM_DATE?='2018-01-01'

ifdef FROM_DATE
download-series-prod: check-output-dir
	python3 download.py --api series-tiempo-prod --cookie $(COOKIE) --output $(OUTPUT_DIR_SDT) --from-date $(FROM_DATE) --end-date $(END_DATE)

download-georef-prod: check-output-dir
	python3 download.py --api georef-prod --cookie $(COOKIE) --output $(OUTPUT_DIR_GR) --from-date $(FROM_DATE) --end-date $(END_DATE)

else
$(error Falta definir FROM_DATE)
endif

check-output-dir:
	if [ ! -d $(OUTPUT_DIR_SDT) ]; then mkdir $(OUTPUT_DIR_SDT); fi
	if [ ! -d $(OUTPUT_DIR_GR) ]; then mkdir $(OUTPUT_DIR_GR); fi



