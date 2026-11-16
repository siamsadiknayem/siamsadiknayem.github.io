#!/usr/bin/env python3
"""
Build gallery albums from a Google Drive folder (so you can upload from your iPhone).

Drive layout (set the parent folder id in content/_data/gallery.yml):

    Website Gallery/                       <- shared "Anyone with the link: Viewer"
      2024-10-12 IEEE ProCon 2024/         <- one folder = one album
        Opening session.jpg                <- file name becomes the caption
        IMG_4021.HEIC                      <- camera names get no caption
        about                              <- optional Google Doc / .txt: album description
      2025-03 Founding the IEEE CS chapter/

  * Album title = folder name; a leading date (YYYY-MM-DD or YYYY-MM) sets the album date.
  * Caption     = the photo's Drive "description" if set, else its file name
                  (camera names like IMG_1234 give no caption). A leading number
                  ("01 Opening session") sets the order and is not shown.
  * Cover       = a photo whose name starts with "cover", else the first photo.

For each photo this downloads it, turns it the right way up, converts iPhone HEIC to
JPEG, shrinks it to 1600 px and removes hidden metadata (including GPS location).
Results go to files/gallery/drive/<album>/ and content/_albums/drive-<album>.md;
both are generated at publish time and not stored in the repository.

Runs in GitHub Actions with the GOOGLE_API_KEY secret. If Drive can't be reached,
the build continues without Drive albums (albums you added by hand still show).
"""
import datetime
import io
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

import yaml
from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:  # HEIC photos will be skipped
    pillow_heif = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.googleapis.com/drive/v3/files"
FOLDER = "application/vnd.google-apps.folder"
GDOC = "application/vnd.google-apps.document"
MAX_SIDE = 1600
OUT_IMG = os.path.join(ROOT, "files", "gallery", "drive")
OUT_MD = os.path.join(ROOT, "content", "_albums")
CAMERA_NAME = re.compile(
    r"^(img|dsc|dscn|dcim|pxl|mvimg|photo|image|screenshot|whatsapp image|signal)[\s_\-]?[\w\-\s:.]*$"
    r"|^\d{8}[_\-]\d{6}.*$|^[0-9a-f]{8}-[0-9a-f]{4}-.*$|^\d+$", re.I)
LEADING_NUM = re.compile(r"^\s*(\d{1,3})[\s._\-)]+(.*)$")
DATE_PREFIX = re.compile(r"^\s*(\d{4}-\d{2}(?:-\d{2})?)[\s._\-–·]*(.*)$")


def get(url, params, key, raw=False):
    params = dict(params, key=key)
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=60) as r:
        data = r.read()
    return data if raw else json.loads(data)


def list_children(folder_id, key):
    out, token = [], None
    while True:
        p = {"q": f"'{folder_id}' in parents and trashed = false",
             "fields": "nextPageToken,files(id,name,mimeType,createdTime,modifiedTime,description,"
                       "imageMediaMetadata(time))",
             "pageSize": "1000", "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"}
        if token:
            p["pageToken"] = token
        d = get(API, p, key)
        out += d.get("files", [])
        token = d.get("nextPageToken")
        if not token:
            return out


def download(file_id, key):
    return get(f"{API}/{file_id}", {"alt": "media", "supportsAllDrives": "true"}, key, raw=True)


def read_text(f, key):
    if f["mimeType"] == GDOC:
        return get(f"{API}/{f['id']}/export", {"mimeType": "text/plain"}, key, raw=True).decode("utf-8", "replace")
    return download(f["id"], key).decode("utf-8", "replace")


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s)[:60] or "album"


def caption_for(f):
    if (f.get("description") or "").strip():
        return f["description"].strip()
    stem = os.path.splitext(f["name"])[0] if "." in f["name"] else f["name"]
    m = LEADING_NUM.match(stem)
    if m:
        stem = m.group(2)
    stem = re.sub(r"\s+", " ", stem.replace("_", " ")).strip()
    if not stem or CAMERA_NAME.match(stem) or stem.lower().startswith("cover"):
        return ""
    return stem


def order_key(f):
    stem = os.path.splitext(f["name"])[0]
    m = LEADING_NUM.match(stem)
    taken = (f.get("imageMediaMetadata") or {}).get("time") or f.get("createdTime") or ""
    return (int(m.group(1)) if m else 10**6, taken, f["name"].lower())


def save_photo(data, path):
    with Image.open(io.BytesIO(data)) as im:
        im = ImageOps.exif_transpose(im)
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        im.convert("RGB").save(path, "JPEG", quality=82, optimize=True, progressive=True)  # no EXIF/GPS


def is_image(f):
    return f["mimeType"].startswith("image/") or f["name"].lower().endswith((".heic", ".heif"))


def main():
    key = os.environ.get("GOOGLE_API_KEY", "").strip()
    cfg_path = os.path.join(ROOT, "content", "_data", "gallery.yml")
    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8")) if os.path.exists(cfg_path) else {}
    parent = (cfg or {}).get("drive_folder") or ""
    if not key or not parent:
        print("Drive gallery: no API key or no drive_folder set — skipping.")
        return 0
    hidden = set(str(h) for h in (cfg.get("hidden") or []))
    overrides = cfg.get("albums") or {}

    # start clean (generated output only)
    shutil.rmtree(OUT_IMG, ignore_errors=True)
    os.makedirs(OUT_IMG, exist_ok=True)
    os.makedirs(OUT_MD, exist_ok=True)
    for name in os.listdir(OUT_MD):
        if name.startswith("drive-") and name.endswith(".md"):
            os.remove(os.path.join(OUT_MD, name))
    manual = {os.path.splitext(n)[0] for n in os.listdir(OUT_MD) if n.endswith(".md")}

    try:
        folders = [f for f in list_children(parent, key) if f["mimeType"] == FOLDER]
    except (urllib.error.URLError, TimeoutError, ValueError) as err:
        print(f"Drive gallery: could not read folder {parent}: {err}")
        return 1

    used, made = set(), 0
    for folder in folders:
        fname = folder["name"].strip()
        if fname in hidden or folder["id"] in hidden or fname.startswith(("_", ".")):
            continue
        m = DATE_PREFIX.match(fname)
        date, title = (m.group(1), m.group(2).strip() or fname) if m else ((folder.get("createdTime") or "")[:10], fname)
        if len(date) == 7:
            date += "-01"
        ov = overrides.get(fname) or {}
        title = ov.get("title", title)
        slug = slugify(title)
        while slug in used or slug in manual:
            slug += "-2"
        used.add(slug)

        try:
            items = list_children(folder["id"], key)
        except (urllib.error.URLError, TimeoutError, ValueError) as err:
            print(f"[{fname}] skipped: {err}")
            continue
        description = ov.get("description", "")
        about = [f for f in items if os.path.splitext(f["name"])[0].strip().lower() in ("about", "description")]
        if about and not description:
            try:
                description = re.sub(r"\s+", " ", read_text(about[0], key)).strip()
            except Exception as err:
                print(f"[{fname}] could not read description: {err}")

        photos = sorted([f for f in items if is_image(f) and f["id"] not in hidden], key=order_key)
        out_dir = os.path.join(OUT_IMG, slug)
        os.makedirs(out_dir, exist_ok=True)
        entries, cover = [], None
        for f in photos:
            rel = f"/files/gallery/drive/{slug}/{f['id']}.jpg"
            try:
                save_photo(download(f["id"], key), os.path.join(out_dir, f"{f['id']}.jpg"))
            except Exception as err:
                print(f"[{fname}] skipped photo {f['name']}: {err}")
                continue
            entry = {"file": rel}
            cap = caption_for(f)
            if cap:
                entry["caption"] = cap
            entries.append(entry)
            if cover is None and f["name"].lower().startswith("cover"):
                cover = rel
        if not entries:
            continue
        try:
            date_val = datetime.date.fromisoformat(date)
        except ValueError:
            date_val = datetime.date.today()
        fm = {"title": title, "date": date_val, "permalink": f"/gallery/{slug}/", "source": "Google Drive",
              "description": description or None, "location": ov.get("location"),
              "cover": cover or entries[0]["file"], "photos": entries}
        fm = {k: v for k, v in fm.items() if v not in (None, "")}
        with open(os.path.join(OUT_MD, f"drive-{slug}.md"), "w", encoding="utf-8") as fh:
            fh.write("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n")
        made += 1
        print(f"[{fname}] {len(entries)} photos → /gallery/{slug}/")
    print(f"Drive gallery: {made} album(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
