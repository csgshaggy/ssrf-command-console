# scripts/checks/docker_check.py

import subprocess


def run():
    try:
        out = subprocess.check_output(
            ["docker", "ps", "--format", "{{.ID}} {{.Ports}}"],
            text=True
        )
        lines = out.strip().splitlines()

        containers = []
        for line in lines:
            cid, *rest = line.split(" ", 1)
            ports = rest[0] if rest else ""
            containers.append({"id": cid, "ports": ports})

        running_backend = any(":8000->" in c["ports"] or ":8000/" in c["ports"] for c in containers)

        status = running_backend
        details = "Backend container running" if status else "No container exposing port 8000"

        return {
            "name": "docker_check",
            "status": status,
            "details": details,
            "data": {"containers": containers},
        }

    except Exception as e:
        return {
            "name": "docker_check",
            "status": False,
            "details": f"docker ps failed: {e}",
            "data": {"containers": []},
        }
