.DEFAULT_GOAL := all

.PHONY: all
all: ## Show the available make targets.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: format
format:  ## Format the code using Ruff.
	poetry run ruff format .
	poetry run ruff check . --fix

.PHONY: lint
lint:  ## Run Python linter using Ruff.
	poetry run ruff check .

.PHONY: install
install:  ## Install the dependencies excluding dev.
	poetry install --only main

.PHONY: install-dev
install-dev:  ## Install the dependencies including dev.
	poetry install

.PHONY: update-template-packages
update-template-packages:  ## Update the project using the initial copier template.
	cd scripts/package_manager_helper && ./update_template_packages.sh && cd ../..

.PHONY: clean
clean: ## Clean the temporary files.
	rm -rf .ruff_cache

.PHONY: test
test:  ## Run the tests.
	echo "Tests not implemented yet"

.PHONY: security-scan	
security-scan:  ## Run the security scan.
	echo "Security scan not implemented yet"
