FROM python:3.5.1-slim

MAINTAINER Sergio Berlotto <sergio.berlotto@gmail.com>

RUN python -V

RUN apt-get update && apt-get upgrade --yes && apt-get install --yes curl
RUN curl -sL https://deb.nodesource.com/setup_0.12 | /bin/bash -
RUN apt-get install --yes nodejs build-essential python-dev git

RUN echo '{ "allow_root": true }' > /root/.bowerrc
RUN npm install -g bower 

WORKDIR /src

COPY . /src

EXPOSE 8080

RUN pip install --upgrade pip ; pip install -r requirements.txt ; rm -rf *.svg .s2i ; bower install

CMD gunicorn wsgi:application --bind=0.0.0.0:8080 --access-logfile=- 
