RUN = poetry run

# ----------------------------------------
# Tests
# ----------------------------------------
test:
	$(RUN) python -m unittest tests/test_*.py

tests/models/%.py: tests/inputs/%.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

serve:
	$(RUN) mkdocs serve
gh-deploy:
	$(RUN) mkdocs gh-deploy
