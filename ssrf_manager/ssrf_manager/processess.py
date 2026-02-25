from .utils import run, color

def check_ports(backend_port, frontend_port):
    print(color("\n🔍 Checking ports...\n", "blue"))

    backend = run(f"ss -tulpn | grep {backend_port}")
    frontend = run(f"ss -tulpn | grep {frontend_port}")

    print(color(f"Backend port {backend_port}:", "yellow"))
    print(backend if backend else color("✔ Free", "green"))

    print(color(f"\nFrontend port {frontend_port}:", "yellow"))
    print(frontend if frontend else color("✔ Free", "green"))

def show_processes():
    print(color("\n📊 Active Python-related processes:\n", "blue"))
    procs = run("ps aux | grep -E 'uvicorn|http.server|python3' | grep -v grep")
    print(procs if procs else color("✔ No active processes.\n", "green"))

def kill_backend():
    run("pkill -f 'uvicorn dashboard_web:app'")

def kill_frontend():
    run("pkill -f 'python3 -m http.server'")
