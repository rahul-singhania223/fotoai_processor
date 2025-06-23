FROM python:3.8.6-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python install --upgrade pip
RUN pip install -r requirements.txt

COPY config config
COPY lib lib
COPY models models

COPY main.py main.py


ENTRYPOINT [ "python", "main.py" ]
