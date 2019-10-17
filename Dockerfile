# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.7.3-stretch

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=webhook_bot Version=0.0.7

ARG BOT_TOKEN
ENV BOT_TOKEN=${BOT_TOKEN}
ARG PROXY_URL
ENV PROXY_URL=${PROXY_URL}
ARG PROXY_USER
ENV PROXY_USER=${PROXY_USER}
ARG PROXY_PASSWORD
ENV PROXY_PASSWORD=${PROXY_PASSWORD}
ARG USER_LIST
ENV USER_LIST=${USER_LIST}

EXPOSE 8000

WORKDIR /app
ADD . /app

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "webhook_bot:webhookbot"]

#RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
#RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
#  && pip install --upgrade pip \
#  && pip install -r requirements.txt \
#  && apk del build-dependencies

# Using pipenv:
# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m webhook_bot"
