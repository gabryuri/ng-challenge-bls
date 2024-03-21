
.PHONY: help
help:
	@echo "****************** COMMANDS  ***********************"
	@echo
	@echo "setup: pip install requirements under the environment folder."
	@echo "lint: Linting using black and SQLFluff."
	@echo "test: runs a pytest on tests folder."
	@echo "deploy: runs the application and shows the necessary logs in a convenient sequence."
	@echo
	@echo "***************************************************"

.PHONY: setup
setup:
	pip install -r environment/requirements_development.txt

.PHONY: lint
lint:
	black . --line-length 120
	sqlfluff fix  --dialect postgres .	

.PHONY: test
test:
	python3 -m pytest ./backend --disable-warnings


.PHONY: deploy up initlogs openbrowser 
deploy: up initlogs openbrowser
up:
	docker compose down && docker compose build && docker compose up -d
initlogs:
	docker compose logs -f initialize-db
openbrowser:
	@echo "Opening Google Chrome at http://127.0.0.1:8080/"
	@google-chrome "http://127.0.0.1:8080/" &
	@google-chrome "http://127.0.0.1:8501/" &

