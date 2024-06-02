test-watch:
	ptw --runner "pytest tests/ -s"

test:
	pytest tests/ -vvs
