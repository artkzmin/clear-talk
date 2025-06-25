venv-run:
	. venv/bin/activate

run:
	python -m src.main

lint:
	ruff check

format:
	ruff format --check

test:
	pytest -s -v

alembic:
	alembic upgrade head

docker-run:
	docker compose -f docker/docker-compose.yml up --build -d

docker-logs:
	docker logs -f clear-talk

docker-clear:
	docker image prune -f
