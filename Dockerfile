FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
RUN poetry config virtualenvs.create false


COPY poetry.lock pyproject.toml ./

COPY scripts/start.sh scripts/
COPY src src/

RUN poetry install


COPY . ./
# COPY src /app/src
# COPY conf /app/conf

# RUN cd /app/
