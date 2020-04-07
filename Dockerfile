FROM python:3.7.6
COPY ./requirements.txt /app/requirements.txt
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt