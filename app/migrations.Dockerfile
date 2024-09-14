FROM python:3.12.5-bookworm

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip install --no-cache-dir poetry==1.8.3 && \
    poetry export --only migrations -f requirements.txt -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

COPY ./alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY ./app /app/app

CMD ["alembic", "upgrade", "head"]