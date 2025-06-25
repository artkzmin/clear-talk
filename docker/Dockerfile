FROM python:3.11.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY alembic.ini alembic.ini
COPY Makefile Makefile

COPY docker/run.sh docker/run.sh
RUN chmod +x docker/run.sh

COPY config/.env config/.env

CMD ["sh", "docker/run.sh"]
