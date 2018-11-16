FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir django-app
WORKDIR /code/django-app
ADD requirement.txt /code/
RUN pip install -r /code/requirement.txt
ADD ./django-app/ /code/django-app/