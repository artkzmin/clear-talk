venv:
	venv/bin/activate

run:
	python -m src.main

alembic:
	alembic upgrade head

docker-run:
	sudo docker compose -f docker/docker-compose.yml up --build -d

docker-logs:
	sudo docker logs -f clear-talk