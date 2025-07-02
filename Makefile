run:
	python -m src.main

lint:
	ruff check

format:
	ruff format --check

test:
	pytest -s -v

coverage:
	coverage run -m pytest
	coverage report

alembic:
	alembic upgrade head

docker-run:
	docker compose -f docker/docker-compose.yml up --build -d

docker-logs:
	docker logs -f clear-talk

docker-clear:
	docker image prune -f

cloc:
	git ls-files | xargs cloc
