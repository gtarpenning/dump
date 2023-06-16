# prebuild
FROM python:3.11-slim

RUN apt update && apt install gcc -y libpq-dev postgresql-server-dev-all

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
