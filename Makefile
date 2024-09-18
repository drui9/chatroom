env := .venv
deps := requirements.txt

run: $(env)
	@$</bin/python main.py

test:
	$(env)/bin/python -m unittest

inst: $(env)
	$</bin/pip install --upgrade -r $(deps)

$(env):
	python -m venv $@

clean:
	rm -rf __pycache__ **/__pycache__ **/**/__pycache__ Logs

