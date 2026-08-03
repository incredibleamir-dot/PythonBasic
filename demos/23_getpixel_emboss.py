"""
Demo 23: Emboss filter using GraphicsWindow.GetPixel / SetPixel.

Reads a photo (demos/demo.jpg) with GraphicsWindow.GetPixel, applies an
emboss kernel, then draws the original and the filtered image side by side.

Run from anywhere:
    python demos/23_getpixel_emboss.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
from smallbasic import GraphicsWindow, ImageList

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.jpg")
if not os.path.exists(IMG):
    print("Put a demo.jpg in the demos/ folder to run this demo.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Load the photo and downscale so per-pixel GetPixel stays quick in a demo.
# ---------------------------------------------------------------------------
src = Image.open(IMG).convert("RGB")
W, H = src.size
scale = min(1.0, 160.0 / W, 110.0 / H)
if scale < 1.0:
    src = src.resize((max(1, int(W * scale)), max(1, int(H * scale))))
W, H = src.size

# ImageList needs a PIL file, so write a temp copy.
_src_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_demo_src.png")
src.save(_src_file)
name = ImageList.LoadImage(_src_file)   # name is the file's basename

# ---------------------------------------------------------------------------
# Window: original on the left, filtered on the right.
# ---------------------------------------------------------------------------
GraphicsWindow.Title = "GetPixel Emboss Filter"
GraphicsWindow.Width = W * 2 + 30
GraphicsWindow.Height = H + 50
GraphicsWindow.PenColor = "Black"
GraphicsWindow.DrawText(10, 8, "Original")
GraphicsWindow.DrawText(W + 20, 8, "Emboss")
GraphicsWindow.Show()
GraphicsWindow.DrawImage(name, 10, 30)      # original (left)

OX, OY = 10, 30  # where the original image was drawn


def pixel_at(x, y):
    """Read one rgb pixel from the drawn image via GetPixel -> '#RRGGBB'."""
    c = GraphicsWindow.GetPixel(OX + x, OY + y)   # e.g. "#12AB34"
    return int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)


# ---------------------------------------------------------------------------
# Read the drawn image one pixel at a time (this is the GetPixel part).
# ---------------------------------------------------------------------------
print(f"Reading {W}x{H} pixels with GetPixel ...")
pix = [[pixel_at(x, y) for x in range(W)] for y in range(H)]

# ---------------------------------------------------------------------------
# Apply an emboss kernel: edges push toward +128 (mid grey).
# ---------------------------------------------------------------------------
KERNEL = [[-1, -1, 0],
          [-1,  0, 1],
          [ 0,  1, 1]]


def emboss(x, y):
    ch = [0, 0, 0]
    for ky in range(3):
        for kx in range(3):
            k = KERNEL[ky][kx]
            if k:
                nx, ny = x + kx - 1, y + ky - 1
                if 0 <= nx < W and 0 <= ny < H:
                    p = pix[ny][nx]
                    ch = [ch[i] + k * p[i] for i in range(3)]
    return tuple(max(0, min(255, v + 128)) for v in ch)


out = Image.new("RGB", (W, H))
for y in range(H):
    for x in range(W):
        out.putpixel((x, y), emboss(x, y))

# ---------------------------------------------------------------------------
# Draw the filtered result side by side on the right.
# ---------------------------------------------------------------------------
_emb_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_demo_emb.png")
out.save(_emb_file)
emb_name = ImageList.LoadImage(_emb_file)
GraphicsWindow.DrawImage(emb_name, W + 20, 30)

# Tidy up the temp files (the images are already in memory).
for f in (_src_file, _emb_file):
    try:
        os.remove(f)
    except OSError:
        pass

print(f"Emboss done for {W}x{H} pixels. Close the window to exit.")
GraphicsWindow.Wait()