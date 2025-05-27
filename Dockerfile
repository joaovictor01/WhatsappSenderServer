FROM python:3.13

WORKDIR /app

COPY src /app

RUN pip install -r requirements.txt

EXPOSE 8081


