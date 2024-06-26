import os
import shlex
import subprocess
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
import httpx
from google.cloud import storage
from dotenv import load_dotenv
from pydantic import BaseModel
import base64


load_dotenv()

SHARED_VOLUME_PATH = os.environ.get("SHARED_VOLUME_PATH", "/uploads")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://fastapi_server")
GCP_BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME", "app")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "project_id")

# Start FastAPI app
app = FastAPI()


class PubSubMessage(BaseModel):
    message: Dict[str, Any]
    subscription: str


@app.get("/")
def root():
    return "pong"


@app.post("/")
def process_video(message: PubSubMessage):
    print(f"Received message: {message}")
    try:
        task_id, file_path = decode_message_data(message)
        edited_file_path = format_edited_file_path(file_path)
        client = storage.Client()

        download_file_from_bucket(file_path, client)
        process_video(file_path, edited_file_path)
        upload_file_to_bucket(edited_file_path, client)
        cleanup(file_path, edited_file_path)

        response = httpx.patch(
            f"{BACKEND_URL}/api/tasks/{task_id}",
        )

        if response.status_code != 200:
            print(f"Failed to update task {task_id} status: {response.text}")
            return HTTPException(status_code=500, detail="Failed to update task status")

        print(f"Task {task_id} status updated successfully")

        return {"status": "success"}
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return HTTPException(status_code=500, detail=str(e))


def decode_message_data(message: PubSubMessage):
    data = base64.b64decode(message.message["data"]).decode("utf-8").strip().split()
    task_id = data[0]
    file_path = data[1]
    return task_id, file_path


def process_video(file_path, edited_file_path):
    ffmpeg_cmd = f"""ffmpeg -i '.{SHARED_VOLUME_PATH}/{file_path}' -i .{SHARED_VOLUME_PATH}/logo.png -filter_complex "[0:v]trim=duration=20,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS[video]; [video][1:v] overlay=W-w-10:H-h-10:enable='between(t,0,1)+between(t,19,20)',trim=duration=20,setpts=PTS-STARTPTS[final]" -map "[final]" -map 0:a? -c:a copy -t 20 '.{SHARED_VOLUME_PATH}/{edited_file_path}' -y"""
    args = shlex.split(ffmpeg_cmd)
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg: {e}")
        return {"status": "failure", "error": str(e)}


def download_file_from_bucket(file_path, storage_client):
    bucket = storage_client.get_bucket(GCP_BUCKET_NAME)
    blob = bucket.blob(file_path)
    blob.download_to_filename(f".{SHARED_VOLUME_PATH}/{file_path}")


def upload_file_to_bucket(file_path, storage_client):
    bucket = storage_client.get_bucket(GCP_BUCKET_NAME)
    blob = bucket.blob(file_path)
    blob.upload_from_filename(f".{SHARED_VOLUME_PATH}/{file_path}")


def format_edited_file_path(file_path):
    edited_file_path = file_path.replace("original_files", "edited_files")
    if not edited_file_path.endswith(".mp4"):
        edited_file_path = os.path.splitext(edited_file_path)[0]
        edited_file_path += ".mp4"
    path_parts = os.path.split(edited_file_path)
    edited_file_path = os.path.join(path_parts[0], path_parts[1])
    return edited_file_path


def cleanup(file_path, edited_file_path):
    os.remove(f".{SHARED_VOLUME_PATH}/{file_path}")
    os.remove(f".{SHARED_VOLUME_PATH}/{edited_file_path}")
