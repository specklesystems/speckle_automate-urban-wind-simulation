FROM python:3.11-slim

RUN pip install poetry

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt && pip install -r requirements.txt
