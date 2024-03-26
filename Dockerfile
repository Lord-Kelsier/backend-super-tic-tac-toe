FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /App
COPY . .

RUN apt-get update
RUN apt-get -y install git
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN ./manage.py migrate
EXPOSE 8000

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]