import os
import shutil

def get_free_space_gb(path="."):
    usage = shutil.disk_usage(path)
    free_gb = usage.free / (1024 ** 3)
    return round(free_gb, 2)
