FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /App
COPY . .
EXPOSE 8000

RUN apt-get update
RUN apt-get -y install git
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt


ENTRYPOINT ["/App/entrypoint.sh"]