FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

ENV PYTHONPATH=/code
EXPOSE 8000