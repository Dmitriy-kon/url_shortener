FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install uv

COPY pyproject.toml ./

COPY scripts/start.sh scripts/
COPY src src/


RUN uv pip install --system -e .


COPY . ./
