import os
import time
from celery import Celery


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
SHARED_VOLUME_PATH = os.environ.get("SHARED_VOLUME_PATH", "/shared_volume")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.edit_video")
def edit_video(file_path: str):
    # TODO: Implement video editing
    return f"Editing video {file_path}..."
