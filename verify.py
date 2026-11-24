#!/usr/bin/env python3
"""Behaviour check for this entry: run main.ts twice and prove the output
is the same valid 1024x1024 PNG both times.

Usage: python3 verify.py
Exits 0 only when every check passes.
"""

import hashlib
import os
import shutil
import struct
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(REPO, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)


def check_png(path, label):
    data = open(path, "rb").read()
    if len(data) > MAX_BYTES:
        fail(f"{label} is {len(data)} bytes, over the {MAX_BYTES} cap")
    if not data.startswith(PNG_MAGIC):
        fail(f"{label} does not start with the PNG signature")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"{label} is {width}x{height}, over {MAX_SIDE}x{MAX_SIDE}")
    print(f"  {label}: {width}x{height}, {len(data)} bytes, PNG magic OK")
    return data, width, height


def main():
    print("Checking entry.png in the repo...")
    data, width, height = check_png(ENTRY, "entry.png")
    if (width, height) != (1024, 1024):
        fail(f"expected 1024x1024, got {width}x{height}")

    runs = []
    for run in (1, 2):
        outdir = os.path.join(REPO, f"out{run}")
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir)
        env = dict(os.environ, MAKEFUN_OUTPUT_DIR=outdir)
        proc = subprocess.run(
            ["node", "main.ts"], cwd=REPO, env=env,
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
            fail(f"run {run}: node main.ts exited {proc.returncode}")
        print(f"  run {run}: {proc.stdout.strip()}")
        out = os.path.join(outdir, "entry.png")
        if not os.path.exists(out):
            fail(f"run {run}: no entry.png written to {outdir}")
        out_data, _, _ = check_png(out, f"run {run} output")
        runs.append(out_data)
        shutil.rmtree(outdir, ignore_errors=True)

    if runs[0] != runs[1]:
        fail("the two runs wrote different bytes (not deterministic)")
    if runs[0] != data:
        fail("a run's output differs from entry.png in the repo")
    print("  determinism: both runs byte-identical to entry.png")
    print("  sha256:", hashlib.sha256(data).hexdigest())
    print("PASS: entry.png is a valid 1024x1024 PNG and main.ts "
          "reproduces it deterministically")


if __name__ == "__main__":
    main()
