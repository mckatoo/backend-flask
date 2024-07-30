test-watch:
	ptw --runner "pytest tests/ -s"

test:
	pytest tests/ -vvs

run:
	flask --app main.py run

run-debug:
	flask --app main.py --debug run

lint:
	ruff check

lint-fix:
	ruff check --fix