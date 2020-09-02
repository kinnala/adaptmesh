default:
	python -m pytest

release:
	python -m pep517.build --source --binary .
	twine upload dist/*

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	@rm -rf *.egg-info/ build/ dist/
