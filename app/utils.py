import os

import secrets
import shutil
from datetime import datetime

def get_free_space_gb(path="."):
    usage = shutil.disk_usage(path)
    free_gb = usage.free / (1024 ** 3)
    return round(free_gb, 2)

def format_datetime(value):
    if not value:
        return ""
    return value.strftime("%H:%M %d.%m.%Y")

def generate_showcase_token():
    return secrets.token_urlsafe(24)

def human_size(num_bytes):
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 ** 2:
        return f"{round(num_bytes / 1024, 1)} KB"
    if num_bytes < 1024 ** 3:
        return f"{round(num_bytes / (1024 ** 2), 1)} MB"
    return f"{round(num_bytes / (1024 ** 3), 2)} GB"

def get_post_size(post):
    text_size = len((post.body_text or "").encode("utf-8"))
    files_size = sum((attachment.size_bytes or 0) for attachment in post.attachments)
    return human_size(text_size + files_size)
