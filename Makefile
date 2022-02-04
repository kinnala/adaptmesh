default:
	python -m pytest
	flake8 .
	isort --check .
	black --check .

release: clean
	python -m pep517.build --source --binary .
	twine upload dist/*

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	@rm -rf *.egg-info/ build/ dist/
