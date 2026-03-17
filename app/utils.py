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