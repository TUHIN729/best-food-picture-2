#!/usr/bin/env python3
# food-picture-01 entry: a photorealistic gourmet smash burger, made to make
# the AI judge hungry. The program copies the picture shipped beside it
# (food.jpg, a 1024x1024 JPEG) to $MAKEFUN_OUTPUT_DIR/entry.png, byte for byte.
#
# The picture: a steaming double smash burger on a dark slate, molten cheddar
# dripping over a charred patty, glossy buttered brioche bun, crisp lettuce
# and ripe tomato, warm bokeh behind. One hero dish, centred, bold shapes
# and warm saturated colour, so it still reads delicious at 300 pixels.
# Standard library only, no network, no model calls, deterministic.

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSET = HERE / "food.jpg"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

# Sanity-check the shipped picture before copying it: it must be a real
# JPEG (FF D8 magic bytes) and inside the gate's 1 MiB cap, so a corrupt
# or oversized asset fails loudly here instead of shipping a bad entry.
data = ASSET.read_bytes()
if data[:2] != b"\xff\xd8":
    raise SystemExit("food.jpg is not a JPEG")
if len(data) > 1_048_576:
    raise SystemExit("food.jpg exceeds the 1 MiB gate limit")

OUT_DIR.mkdir(parents=True, exist_ok=True)
out_path = OUT_DIR / "entry.png"
out_path.write_bytes(data)

# Size-match guard: read the output back and confirm it is byte-for-byte
# identical to the shipped asset, so a truncated or partial write can never
# pass silently as a valid entry.
written = out_path.read_bytes()
if len(written) != len(data) or written != data:
    raise SystemExit("entry.png does not match food.jpg byte-for-byte")
