FROM python:3.10-bullseye

LABEL maintainer="francisco-javier.crabiffosse.ext@eurocontrol.int"

RUN apt-get --allow-releaseinfo-change update --fix-missing -y; apt-get upgrade -y

RUN apt-get install supervisor -y

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /etc/supervisor/conf.d
RUN mkdir -p /supervisor

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r ./requirements.txt

COPY ./met_update /app/met_update
COPY ./supervisor/met_update.conf /etc/supervisor/conf.d/met_update.conf
COPY ./supervisor/supervisord.conf /etc/supervisor/supervisord.conf

ENV PYTHONPATH /app

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
