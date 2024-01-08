all:
	@echo '## Make commands ##'
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

lint:
	mypy --package imshow
	ruff format --check
	ruff check

format:
	ruff format
	ruff check --fix

clean:
	rm -rf build dist *.egg-info

publish: clean
	pip install -e .
	git pull origin main
	git tag v$(shell python -m imshow --version | awk '{print $$2}')
	git push origin main --tags
	python -m build --sdist --wheel
	python -m twine upload dist/imshow-*
