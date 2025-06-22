run:
	. venv/bin/activate && python -m src.main

alembic:
	. venv/bin/activate && alembic upgrade head
