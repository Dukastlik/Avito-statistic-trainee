FROM python:3.8.6-buster

ENV PYTHONBUFFERED 1


WORKDIR /usr/src/avito_stat/app
EXPOSE 8001

COPY . .
RUN pip install --no-cache-dir -r requirements.txt


CMD uvicorn main:app --host 0.0.0.0 --port 8001 --reload
