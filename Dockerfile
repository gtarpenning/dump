FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

RUN pip install --upgrade pip && \
    pip install scikit-learn openai

COPY . .

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app
