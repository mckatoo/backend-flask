test-watch:
	ptw --runner "pytest tests/ -s"

test:
	pytest tests/ -vvs

run:
	flask --app main.py --debug run