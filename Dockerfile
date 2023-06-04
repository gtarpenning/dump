FROM gtarpenning/prebuild-flask:latest

COPY . .

CMD [ "python3", "-m" , "flask", "--app", "main.py", "run", "--host=0.0.0.0"]
