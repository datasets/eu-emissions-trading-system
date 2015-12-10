all:
	python scripts/process.py

clean:
	rm data/* cache/*

.PHONY: clean
