import os
import subprocess
import sys

def run_command(cmd):
    print(f"[EXEC] {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr.strip()}")
    else:
        print(f"[SUCCESS] {result.stdout.strip()}")
    return result.returncode

def main(): 