all:
	python scripts/process.py

clean:
	rm data/co2-ppm-vostok.csv cache/co2-ppm-vostok.csv

.PHONY: clean
