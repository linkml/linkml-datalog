RUN = poetry run

# ----------------------------------------
# Tests
# ----------------------------------------
test:
	$(RUN) python -m unittest discover -p 'test_*.py'

tests/models/%.py: tests/inputs/%.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@
