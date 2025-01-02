.PHONY: test_all

test_all:
	python3 -m pytest -o log_cli=True verif/py/
