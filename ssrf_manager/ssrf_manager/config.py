import os
import click

DEFAULT_BACKEND_PORT = 5001
DEFAULT_FRONTEND_PORT = 8000

def get_project_root():
    return os.path.expanduser("~/SSRF_CONSOLE")

def get_dashboard_dir():
    return os.path.join(get_project_root(), "dashboard")

def get_venv_activate():
    return os.path.join(get_project_root(), "venv/bin/activate")

class Config:
    def __init__(self, backend_port=None, frontend_port=None, headless=False):
        self.backend_port = backend_port or DEFAULT_BACKEND_PORT
        self.frontend_port = frontend_port or DEFAULT_FRONTEND_PORT
        self.headless = headless

def load_config(backend_port, frontend_port, headless):
    return Config(
        backend_port=backend_port,
        frontend_port=frontend_port,
        headless=headless,
    )
