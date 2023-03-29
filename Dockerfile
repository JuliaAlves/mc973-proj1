FROM python:3.7.12-alpine

WORKDIR /app

COPY ./main.py /app/main.py
COPY ./services /app/services

ENV TESTS_PATH=/app/test

CMD [ "python3", "main.py"]