run:
	python3 main.py --query "iPhone 16 Pro, 128GB" --country "US"

test:
	python3 tests/run_all_tests.py

all: test run 