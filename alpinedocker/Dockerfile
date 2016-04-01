FROM python:3.5.1-alpine

MAINTAINER Sergio Berlotto <sergio.berlotto@gmail.com>

ENV APP_USER pythonuser
ENV APP_ROOT /home/$APP_USER/src

# Install basic environment
RUN apk add --no-cache build-base git nodejs && \
    adduser -u 1001 -G root -D -h /home/$APP_USER -s /bin/sh $APP_USER && \
    echo '{ "allow_root": true }' > /home/$APP_USER/.bowerrc && \
    npm install -g bower && \
    npm cache clean 

# Install app and ensure ownership
RUN git clone https://github.com/ProgramadorLivre/issue-tracker.git $APP_ROOT && \
    cd $APP_ROOT && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf *.svg .s2i && \
    bower install && \
    bower cache clean && \
    chown -R 1001:0 /home/$APP_USER/ && \
    chmod -R g+rw /home/$APP_USER/ && \
    find /home/$APP_USER/ -type d -exec chmod g+x {} + && \
    npm uninstall bower && \
    apk del build-base git nodejs -r --purge && \
    rm -rf /usr/lib/node_modules


# Getting ready to run...
USER $APP_USER
WORKDIR $APP_ROOT
EXPOSE 8080

# Run
CMD gunicorn wsgi:application --bind=0.0.0.0:8080 --access-logfile=-
