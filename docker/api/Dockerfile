ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y supervisor && apt-get install -y vim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ARG API_PORT
ENV API_PORT ${API_PORT}
EXPOSE ${API_PORT}
CMD uvicorn v1.api:app --host=0.0.0.0 --port ${API_PORT} --reload
