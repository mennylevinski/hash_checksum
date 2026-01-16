# -*- coding: utf-8 -*-

"""
Author: Menny Levinski
"""

import threading
import itertools
import time
import hashlib
import os
import sys
import json

# Spinning dots while threading
class Spinner:
    def __init__(self, message="Generating checksum"):
        self.message = message
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        # Print message once
        sys.stdout.write(self.message)
        sys.stdout.flush()

        while not self._stop_event.is_set():
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.4)

        # Finish line cleanly
        sys.stdout.write("\n")
        sys.stdout.flush()

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

# 🔒 Static file path
FILE_PATH = r"C:\Users\User\Desktop\SecuditorLite.exe"

def calculate_file_hashes(file_path):
    if not os.path.isfile(file_path):
        return {"error": f"File not found: {file_path}"}

    hash_algos = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256(),
        "SHA512": hashlib.sha512(),
    }

    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                for algo in hash_algos.values():
                    algo.update(chunk)

        return {name: algo.hexdigest() for name, algo in hash_algos.items()}

    except Exception as e:
        return {"error": str(e)}

def generate_hash_report(file_path, output_json=False):
    result = calculate_file_hashes(file_path)

    if output_json:
        return json.dumps({"file": file_path, "hashes": result}, indent=4)
    else:
        report = f"\nFile: {file_path}\n"
        for algo, digest in result.items():
            report += f"{algo}: {digest}\n"
        return report

# --- Output ---
if __name__ == "__main__":
    spinner = Spinner("Generating checksum")
    spinner.start()
    time.sleep(2)
    # Actual work
    report = generate_hash_report(FILE_PATH)

    spinner.stop()
    print(report)
    input("Press Enter to exit")
