test-watch:
	ptw --runner "pytest tests/ -s"

test:
	pytest tests/ -vvs

run:
	flask --app main.py run

run-debug:
	flask --debug --app main.py run