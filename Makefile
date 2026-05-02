.PHONY: test

test:
	@for d in weeks/week-*/tests; do \
		echo "Running tests in $$d "; \
		python -m pytest -q $$d || exit 1; \
	done