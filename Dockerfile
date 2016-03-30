FROM python:3.5.1-slim

MAINTAINER Sergio Berlotto <sergio.berlotto@gmail.com>
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

EXPOSE 8080

RUN apt-get update && apt-get upgrade --yes && apt-get install --yes curl
RUN curl -sL https://deb.nodesource.com/setup_0.12 | /bin/bash -
RUN apt-get install --yes nodejs build-essential git 

RUN echo '{ "allow_root": true }' > /root/.bowerrc
RUN npm install -g bower 

RUN mkdir /src

#Add a non root user to run services
RUN useradd -c 'Python app user' -m -d /home/pythonuser -s /bin/bash pythonuser
ENV HOME /home/pythonuser

WORKDIR /src

RUN git clone https://github.com/ProgramadorLivre/issue-tracker.git /src

RUN pip install --upgrade pip && pip install -r requirements.txt ; rm -rf *.svg .s2i ; 

RUN chown -R pythonuser.pythonuser /src
USER pythonuser

RUN bower install

RUN python -V

CMD gunicorn wsgi:application --bind=0.0.0.0:8080 --access-logfile=- 
