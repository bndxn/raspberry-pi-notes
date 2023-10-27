test: 
	pytest

format:
	pydocstyle src
	mypy src