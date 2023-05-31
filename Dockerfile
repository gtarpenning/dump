FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

RUN pip install --upgrade pip && \
    pip install scikit-learn openai

COPY . .

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

CMD ["uvicorn", "main:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
