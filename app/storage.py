import os
import uuid

from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")

def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file_storage):
    ensure_upload_dir()


    original_name = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{original_name}"

    absolute_path = os.path.join(UPLOAD_DIR, unique_name)
    file_storage.save(absolute_path)

    
    return {
        "original_name": original_name,
        "stored_name": unique_name,
        "relative_path": os.path.join("data", "uploads", unique_name),
        "size_bytes": os.path.getsize(absolute_path),
        "mime_type": file_storage.mimetype,
    }

def delete_file(relative_path):
    absolute_path = os.path.join(BASE_DIR, relative_path)

    if os.path.exists(absolute_path):
        os.remove(absolute_path)