.PHONY: test_all, clean

test_all:
	python3 -m pytest -v -o log_cli=True verif/py/

clean:
	rm -rf sim_build
