FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
COPY ./credentials.json /code/credentials.json

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

ENV PYTHONPATH=/code
ENV SHARED_VOLUME_PATH=/uploads
ENV BACKEND_URL=https://back-cloudrun-2nsyei5otq-uc.a.run.app
ENV GCP_BUCKET_NAME=drone-racing-league
ENV GOOGLE_CLOUD_PROJECT=misw4204-g6
EXPOSE 8000
CMD ["gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "tasks:app", "--bind", "0.0.0.0:8000", "--preload", "--log-level=debug", "--timeout", "120"]