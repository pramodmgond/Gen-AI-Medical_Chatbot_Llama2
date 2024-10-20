#"""      This file is used to build a Docker image for your Python application.
# It defines the environment in which your app will run,
#             including the necessary dependencies and commands to execute.""""
#
FROM python:3.8.5-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]