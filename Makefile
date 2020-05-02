clean:
	rm -rf dist/ humax.egg-info/ build/

package:
	python3 setup.py sdist bdist_wheel

pypi-upload-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-upload:
	python3 -m twine upload dist/*
