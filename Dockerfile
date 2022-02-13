FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/jamiya

COPY ./jamiya/requirements.txt /usr/src/jamiya/

COPY . /usr/src/jamiya/

RUN pip install -r requirements.txt



