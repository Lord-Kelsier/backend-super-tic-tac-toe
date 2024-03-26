FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /App
COPY . .

RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python manage.py createsuperuser --username admin --email econtreraslazcano@uc.cl
RUN python ./manage.py migrate

CMD ["python", "./manage.py", "runserver", "localhost:8000"]