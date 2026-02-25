import subprocess
import os
import shutil

def run(cmd):
    return subprocess.getoutput(cmd)

def color(text, c):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    return f"{colors.get(c,'')}{text}{colors['reset']}"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def rotate_log(path, max_size=2_000_000):
    if os.path.exists(path) and os.path.getsize(path) > max_size:
        shutil.move(path, path + ".1")
