FROM python:3.12-slim


# use this if you're using image/headless OpenCV only
RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY config config
COPY lib lib
COPY models models

COPY main.py main.py


ENTRYPOINT [ "python", "main.py" ]
