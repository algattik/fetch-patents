FROM python:3.11-slim-bullseye AS base

RUN set -x

RUN apt-get update \
    && apt-get -y install \
        curl \
        net-tools \
        procps \
        build-essential \
        wget \
        git

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN set +x

CMD bash
