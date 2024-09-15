FROM python:3.12.5-bookworm AS deps

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry export --only main -f requirements.txt -o requirements.txt

FROM amazonlinux:2 AS release

RUN yum install -y \
    gcc \
    mysql-devel \
    python3 \
    python3-devel \
    && yum clean all

RUN python3 -m ensurepip --upgrade \
    && pip3 install --upgrade pip \
    && pip3 install awslambdaric

COPY --from=deps /app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /var/task

CMD [ "app.main.handler" ]