FROM python:3.9.6-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y build-essential python3-dev default-libmysqlclient-dev \
    && apt-get clean
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/