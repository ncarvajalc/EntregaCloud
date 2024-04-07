import os
import shlex
import subprocess
import uuid
from celery import Celery


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
SHARED_VOLUME_PATH = os.environ.get("SHARED_VOLUME_PATH", "/uploads")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.edit_video")
def edit_video(file_path: str):
    edited_file_path = format_edited_file_path(file_path)
    ffmpeg_cmd = f"""ffmpeg -i '{file_path}' -i .{SHARED_VOLUME_PATH}/logo.png -filter_complex "[0:v]trim=duration=20,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS[video]; [video][1:v] overlay=W-w-10:H-h-10:enable='between(t,0,1)+between(t,19,20)',trim=duration=20,setpts=PTS-STARTPTS[final]" -map "[final]" -map 0:a? -c:a copy -t 20 '{edited_file_path}' -y"""
    args = shlex.split(ffmpeg_cmd)
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg: {e}")
        return {"status": "failure", "error": str(e)}

    # TODO: Cambiar el estado de la tarea a "success" en la base de datos

    return {"status": "success", "edited_file_path": edited_file_path}


def format_edited_file_path(file_path):
    edited_file_path = file_path.replace("original_files", "edited_files")
    if not edited_file_path.endswith(".mp4"):
        edited_file_path = os.path.splitext(edited_file_path)[0]
        edited_file_path += ".mp4"
    unique_id = str(uuid.uuid4())
    path_parts = os.path.split(edited_file_path)
    edited_file_path = os.path.join(path_parts[0], unique_id + "_" + path_parts[1])
    return edited_file_path
