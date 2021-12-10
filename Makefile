RUN = poetry run

# ----------------------------------------
# Tests
# ----------------------------------------
test:
	$(RUN) python -m unittest discover -p 'test_*.py'
