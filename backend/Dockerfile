FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/app /code/app
COPY ./app/credentials.json /code/credentials.json

ENV PYTHONPATH=/code
ENV PROJECT_NAME="Entrega Cloud"
ENV MODE=development
ENV DATABASE_URL="postgresql://postgres:postgres@10.64.96.3:5432/cloud" 
ENV SHARED_VOLUME_PATH=/uploads
ENV HOST=http://localhost:8001
ENV GCP_BUCKET_NAME=drone-racing-league
ENV GOOGLE_APPLICATION_CREDENTIALS=/code/credentials.json
ENV GOOGLE_CLOUD_PROJECT=misw4204-g6
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host" , "0.0.0.0"]
