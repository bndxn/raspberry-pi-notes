test:
	pytest

format:
	pydocstyle src
	mypy --ignore-missing-imports src
