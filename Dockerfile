FROM python:3.11.4-slim-buster

WORKDIR /usr/src/mysite

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /usr/src/mysite/
RUN pip install -r requirements.txt

COPY mysite/ /usr/src/mysite

CMD ["bash", "-c", "/usr/src/mysite/startup.sh"]