ALEMBIC := alembic
PIP := pip

install:
	@$(PIP) install -r requirements/common.txt

install-dev:
	@$(PIP) install -r requirements/dev.txt

run-migrations:
	$(ALEMBIC) upgrade head
