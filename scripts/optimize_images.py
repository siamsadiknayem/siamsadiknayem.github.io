#!/usr/bin/env python3
"""
Prepare gallery photos for the web (runs automatically when the site is published).

For every image under files/gallery/ and files/images/posts/:
  * rotates it the right way up (phone photos store rotation separately),
  * shrinks it to at most 1600 px on the long side,
  * removes hidden metadata, including GPS location from phone cameras,
  * re-saves JPEGs at quality 82.

It only changes the copy being published. The photos in your repository
stay exactly as you uploaded them.

Run locally (optional):  python3 scripts/optimize_images.py
"""
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is needed: pip install pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDERS = [os.path.join(ROOT, "files", "gallery"), os.path.join(ROOT, "files", "images", "posts")]
MAX_SIDE = 1600
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def process(path):
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)          # fix rotation
        if max(im.size) > MAX_SIDE:
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        ext = os.path.splitext(path)[1].lower()
        if ext in (".jpg", ".jpeg"):
            im.convert("RGB").save(path, "JPEG", quality=82, optimize=True, progressive=True)
        elif ext == ".png":
            im.save(path, "PNG", optimize=True)    # saved without metadata
        else:
            im.save(path, "WEBP", quality=82)


def main():
    count = 0
    for folder in FOLDERS:
        for dirpath, dirs, names in os.walk(folder):
            dirs[:] = [d for d in dirs if not (folder.endswith('gallery') and d == 'drive')]  # Drive photos already prepared
            for name in names:
                if os.path.splitext(name)[1].lower() in EXTS:
                    try:
                        process(os.path.join(dirpath, name)); count += 1
                    except Exception as err:  # keep going; a bad file shouldn't stop publishing
                        print(f"skipped {name}: {err}")
    print(f"optimised {count} image(s)")


if __name__ == "__main__":
    main()
