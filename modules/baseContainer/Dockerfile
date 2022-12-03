FROM arm64v8/python:3.9-alpine3.16

WORKDIR /usr/bin/app

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev i2c-tools g++\
    && apk add libffi-dev
COPY requirements.txt ./
# RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt