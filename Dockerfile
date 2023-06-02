FROM python:3.11-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "main.py", "run", "--host=0.0.0.0"]
