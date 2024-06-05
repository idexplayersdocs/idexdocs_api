.PHONY: dev prod test

test:
	@echo "Installing dependencies for test environment..."
	@pip install -r requirements/test.txt > /dev/null 2>&1
	@echo "Done!"
dev:
	@echo "Installing dependencies for development environment..."
	@pip install -r requirements/dev.txt > /dev/null 2>&1
	@echo "Done!"
prod:
	@echo "Installing dependencies for production environment..."
	@pip install -r requirements/prod.txt > /dev/null 2>&1
	@echo "Done!"

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .tox/
	rm -rf htmlcov
	pip install -r requirements/test.txt --upgrade --no-cache > /dev/null 2>&1
