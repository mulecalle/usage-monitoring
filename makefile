dependencies:
	pip3 install -r requirements.txt

run:
	python3 src/main.py

mock-server:
	python3 mocks/server.py

test:
	PYTHONPATH=. pytest tests/ -v

test-coverage:
	PYTHONPATH=. pytest tests/ --cov=src --cov-report=term-missing -v

