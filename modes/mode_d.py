import os
import re
import hashlib
import requests
from datetime import datetime


class ModeDRunner:
    """
    Recursive Discovery Mode (Mode D)
    - Starts from a seed list of paths
    - Requests each path via the vulnerable parameter
    - Extracts new paths from responses
    - Recursively explores newly discovered paths
    """

    def __init__(
        self,
        base_url,
        param,
        seeds,
        output_dir="results/moded",
        timeout=8,
        max_depth=4,
        max_paths=2000,
    ):
        self.base_url = base_url.rstrip("/")
        self.param = param
        self.seeds = seeds
        self.output_dir = output_dir
        self.timeout = timeout
        self.max_depth = max_depth
        self.max_paths = max_paths

        os.makedirs(self.output_dir, exist_ok=True)

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

    def classify(self, response, baseline_len):
        if response is None:
            return "ERROR"

        length = len(response.text)

        if response.status_code == 200:
            if length > baseline_len + 50:
                return "INTERESTING"
            elif length > baseline_len + 5:
                return "SLIGHTLY_INTERESTING"
            else:
                return "BORING"
        elif response.status_code in (401, 403):
            return "BLOCKED"
        else:
            return "INVALID"

    def save_result(self, path, content, depth):
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', path)
        filename = os.path.join(self.output_dir, f"{depth}_{safe_name}.txt")

        sha = hashlib.sha256(content.encode(errors="ignore")).hexdigest()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(filename, "w", encoding="utf-8", errors="ignore") as f:
            f.write(f"[Path]: {path}\n")
            f.write(f"[Depth]: {depth}\n")
            f.write(f"[Timestamp]: {timestamp}\n")
            f.write(f"[SHA256]: {sha}\n\n")
            f.write(content)

        print(f"    └─ Saved to: {filename}")

    def extract_paths(self, content):
        found = set()
        for match in re.findall(r'(/[a-zA-Z0-9_\-./]+)', content):
            if len(match) > 1:
                found.add(match)
        return found

    def run(self):
        print("\n[+] Starting Mode D (Recursive Discovery)...\n")

        baseline = self.fetch("this_path_should_not_exist_123456")
        baseline_len = len(baseline.text) if baseline else 0
        print(f"[i] Baseline length: {baseline_len}")

        # queue entries: (path, depth)
        queue = [(p, 0) for p in self.seeds]
        seen = set()
        total_processed = 0

        while queue:
            path, depth = queue.pop(0)

            if path in seen:
                continue
            seen.add(path)

            if depth > self.max_depth:
                continue

            if total_processed >= self.max_paths:
                print("[!] Reached max_paths limit, stopping.")
                break

            total_processed += 1

            print(f"[>] Depth {depth} | Testing: {path}")
            response = self.fetch(path)
            classification = self.classify(response, baseline_len)
            print(f"    └─ Classification: {classification}")

            if classification in ("INTERESTING", "SLIGHTLY_INTERESTING") and response is not None:
                self.save_result(path, response.text, depth)

                new_paths = self.extract_paths(response.text)
                for p in new_paths:
                    if p not in seen:
                        print(f"    └─ Discovered path: {p}")
                        queue.append((p, depth + 1))

        print("\n[+] Mode D Complete.\n")
