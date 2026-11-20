#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119:
"Sum up 19 November's world news in one image".

The image is prepared ahead of time and shipped in this repository
as entry.png. This program only copies it, byte for byte, to the
output directory, so both runs of the entry write exactly the same
bytes. Standard library only; no network, no clock, no randomness.

Run it with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The image lands at out/entry.png.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    # Fail loudly instead of writing a broken entry: the shipped image
    # must exist and must not be empty.
    try:
        source_size = os.path.getsize(SOURCE)
    except OSError as exc:
        raise SystemExit("entry.png missing next to main.py: %s" % exc)
    if source_size == 0:
        raise SystemExit("entry.png is empty, refusing to write an empty entry")
    source_hash = sha256_of(SOURCE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)

    # The copy must be exact: same bytes in, same bytes out. Compare
    # the hash, not just the size, so a truncated copy cannot pass.
    if sha256_of(target) != source_hash:
        raise SystemExit("entry.png copy mismatch: hash differs from source")
    print("wrote %s (%d bytes, sha256 %s)" % (target, source_size, source_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
