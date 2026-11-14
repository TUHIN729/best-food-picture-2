"""Copy food.jpg byte-for-byte to entry.png in the output directory.

The picture is finished already; this script does no image processing.
It only copies the bytes and verifies the copy, so entry.png is exactly
the JPEG stored in food.jpg.
"""

import os
import sys

MAX_BYTES = 1024 * 1024  # 1 MiB


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "food.jpg")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        data = f.read()
    print("input: %s (%d bytes)" % (src, len(data)))
    if len(data) > MAX_BYTES:
        print("error: input is %d bytes, over the 1 MiB limit" % len(data), file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    print("output: %s" % dst)

    with open(dst, "rb") as f:
        copied = f.read()
    if copied != data:
        print("error: output differs from input", file=sys.stderr)
        return 1
    # The size limit applies to the file as submitted too, so re-check
    # the bytes actually on disk, not just the bytes we meant to write.
    if len(copied) > MAX_BYTES:
        print("error: output is %d bytes, over the 1 MiB limit" % len(copied), file=sys.stderr)
        return 1
    print("verified: output matches input byte-for-byte (%d bytes)" % len(copied))
    return 0


if __name__ == "__main__":
    sys.exit(main())
