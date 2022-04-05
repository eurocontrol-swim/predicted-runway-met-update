FROM python:3.9-buster

LABEL maintainer="francisco-javier.crabiffosse.ext@eurocontrol.int"

ADD ./met_update /app/met_update
ADD requirements.txt /app/requirements.txt

RUN mkdir "/data"
RUN mkdir "/data/metar"
RUN mkdir "/data/taf"

VOLUME ["/data"]

WORKDIR /app
RUN pip install -r ./requirements.txt

ENV PYTHONPATH /app

ENTRYPOINT ["python", "./met_update/main.py"]
