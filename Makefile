.PHONY: setup test lint clean run

setup:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/

lint:
	black src tests
	isort src tests
	pylint src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

run:
	streamlit run src/ui/app.py
