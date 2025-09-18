FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY config config
COPY lib lib
COPY models models

RUN export PYTHONPATH=.

COPY main.py main.py


ENTRYPOINT [ "python", "main.py" ]
