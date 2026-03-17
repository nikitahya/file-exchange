import os
import uuid

from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1 GB

def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_single_file(file_storage):
    ensure_upload_dir()

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size > MAX_FILE_SIZE:
        raise ValueError("File too large")

    original_name = file_storage.filename
    safe_name = secure_filename(original_name)

    ext = ""
    if "." in safe_name:
        ext = "." + safe_name.rsplit(".", 1)[1]

    unique_name = f"{uuid.uuid4().hex}{ext}"

    absolute_path = os.path.join(UPLOAD_DIR, unique_name)
    file_storage.save(absolute_path)

    return {
        "original_name": original_name,
        "stored_name": unique_name,
        "relative_path": os.path.join("data", "uploads", unique_name),
        "size_bytes": os.path.getsize(absolute_path),
        "mime_type": file_storage.mimetype,
    }

def save_files(file_storages):
    return [save_single_file(file_storage) for file_storage in file_storages]

def delete_file(relative_path):
    absolute_path = os.path.join(BASE_DIR, relative_path)

    if os.path.exists(absolute_path):
        os.remove(absolute_path)