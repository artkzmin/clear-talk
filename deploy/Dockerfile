FROM python:3.11.9

WORKDIR /app

COPY ../requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY ../src .
COPY ../config .
COPY ../alembic .
COPY ../Makefile .
CMD ["make", "run"]
