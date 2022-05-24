FROM python:3.10-bullseye

LABEL maintainer="francisco-javier.crabiffosse.ext@eurocontrol.int"

WORKDIR /app

COPY ./met_update /app/met_update

COPY requirements.txt /app/requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH /app

CMD ["python", "/app/met_update/main.py"]
