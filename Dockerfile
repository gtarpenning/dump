FROM gtarpenning/prebuild-flask:latest

WORKDIR /engine
COPY ./engine /engine

CMD [ "python3", "-m" , "flask", "--app", "main.py", "run", "--host=0.0.0.0", "--port=8080"]
