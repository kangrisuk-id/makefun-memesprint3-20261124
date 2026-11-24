#!/usr/bin/env python3
"""Meme Sprint 3 entry: emit the pre-built meme image as entry.png.

The meme itself ships next to this program as meme.bin (the exact bytes of
the judged image). This program only locates that payload and copies it to
the grader's output directory, trying each candidate directory in order.
"""

import os
import sys

PAYLOAD_NAME = "meme.bin"
OUTPUT_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def find_payload():
    """Return the path of meme.bin, searching the usual locations."""
    candidates = []
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        candidates.append(bot_dir)
    candidates.append(os.path.dirname(os.path.abspath(__file__)))
    candidates.append(os.getcwd())
    for directory in candidates:
        path = os.path.join(directory, PAYLOAD_NAME)
        if os.path.isfile(path):
            return path
    return None


def output_dirs():
    """Candidate output directories, most preferred first."""
    dirs = []
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        dirs.append(out_dir)
    dirs.append("/output")
    dirs.append("./output")
    return dirs


def main():
    payload_path = find_payload()
    if payload_path is None:
        print("meme.bin not found next to the program", file=sys.stderr)
        return 1
    with open(payload_path, "rb") as handle:
        data = handle.read()
    if not data.startswith(PNG_MAGIC):
        print("meme.bin is not a PNG image", file=sys.stderr)
        return 1
    last_error = None
    for directory in output_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, OUTPUT_NAME)
            with open(target, "wb") as handle:
                handle.write(data)
            written = os.path.getsize(target)
            if written != len(data):
                raise OSError(
                    "short write: %d of %d bytes" % (written, len(data))
                )
            print("wrote %s (%d bytes)" % (target, len(data)))
            return 0
        except OSError as error:
            last_error = error
    print("could not write entry.png: %s" % last_error, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
