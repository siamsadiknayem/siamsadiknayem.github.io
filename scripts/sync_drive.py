#!/usr/bin/env python3
"""
Sync Google Drive course folders into the website.

For every course in content/_data/courses.yml that has a `drive_folder`, this lists the
files in that Drive folder (and one level of sub-folders) and writes
content/_data/drive/<slug>.json. The course pages are built from those files, so
adding, replacing, renaming or deleting a file in Drive changes the website on
the next build.

Runs automatically in GitHub Actions (.github/workflows/build-and-deploy.yml).
Needs a Google API key in the repository secret GOOGLE_API_KEY. The folders must
be shared as "Anyone with the link can view".

Safe by design: if Drive cannot be reached, the existing JSON is left untouched
so the site keeps showing the last good list.

Run locally:  GOOGLE_API_KEY=... python3 scripts/sync_drive.py
"""
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is needed: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.googleapis.com/drive/v3/files"
FOLDER = "application/vnd.google-apps.folder"
SHORTCUT = "application/vnd.google-apps.shortcut"

# Google-native files: (short type, view URL, export-as-PDF URL)
GOOGLE_NATIVE = {
    "application/vnd.google-apps.presentation": (
        "gslides",
        "https://docs.google.com/presentation/d/{id}/view",
        "https://docs.google.com/presentation/d/{id}/export/pdf"),
    "application/vnd.google-apps.document": (
        "gdoc",
        "https://docs.google.com/document/d/{id}/view",
        "https://docs.google.com/document/d/{id}/export?format=pdf"),
    "application/vnd.google-apps.spreadsheet": (
        "gsheet",
        "https://docs.google.com/spreadsheets/d/{id}/view",
        None),
}


def api_list(folder_id, key):
    """Return all non-trashed children of a Drive folder."""
    files, token = [], None
    while True:
        params = {
            "q": f"'{folder_id}' in parents and trashed = false",
            "fields": "nextPageToken,files(id,name,mimeType,modifiedTime,size,shortcutDetails)",
            "pageSize": "1000",
            "orderBy": "name_natural",
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
            "key": key,
        }
        if token:
            params["pageToken"] = token
        url = API + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.load(resp)
        files.extend(data.get("files", []))
        token = data.get("nextPageToken")
        if not token:
            return files


def describe(f, folder_name=""):
    fid, mime, name = f["id"], f["mimeType"], f["name"]
    if mime in GOOGLE_NATIVE:
        ext, view, dl = GOOGLE_NATIVE[mime]
        view = view.format(id=fid)
        dl = dl.format(id=fid) if dl else None
    else:
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        view = f"https://drive.google.com/file/d/{fid}/view"
        dl = f"https://drive.google.com/uc?export=download&id={fid}"
    base = name if mime in GOOGLE_NATIVE or "." not in name else name.rsplit(".", 1)[0]
    title = re.sub(r"\s+", " ", base.replace("_", " ")).strip()
    return {
        "id": fid,
        "name": name,
        "title": title,
        "mimeType": mime,
        "ext": ext,
        "folder": folder_name,
        "modifiedTime": (f.get("modifiedTime") or "")[:19] + "Z" if f.get("modifiedTime") else "",
        "size": int(f["size"]) if f.get("size") else None,
        "view": view,
        "download": dl,
    }


def sync_course(slug, folder_id, key):
    out = []
    for f in api_list(folder_id, key):
        mime = f["mimeType"]
        if mime == FOLDER:  # one level of sub-folders, e.g. "Lab manuals"
            for g in api_list(f["id"], key):
                if g["mimeType"] not in (FOLDER, SHORTCUT):
                    out.append(describe(g, f["name"]))
        elif mime == SHORTCUT:
            continue  # shortcuts point elsewhere; add the real file instead
        else:
            out.append(describe(f))
    out.sort(key=lambda d: (d["folder"].lower(), d["name"].lower()))
    return out


def main():
    key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not key:
        print("GOOGLE_API_KEY is not set: skipping Drive sync (site keeps the last saved lists).")
        return 0

    with open(os.path.join(ROOT, "content", "_data", "courses.yml"), encoding="utf-8") as fh:
        courses = yaml.safe_load(fh) or []

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.join(ROOT, "content", "_data", "drive"), exist_ok=True)
    problems = 0
    for c in courses:
        folder = (c.get("drive_folder") or "").strip()
        if not folder:
            continue
        slug = c["slug"]
        path = os.path.join(ROOT, "content", "_data", "drive", f"{slug}.json")
        try:
            files = sync_course(slug, folder, key)
        except (urllib.error.URLError, TimeoutError, ValueError) as err:
            problems += 1
            detail = err.read().decode()[:300] if isinstance(err, urllib.error.HTTPError) else str(err)
            print(f"[{slug}] could not read Drive folder {folder}: {detail}")
            print(f"[{slug}] keeping the previous list.")
            continue
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"folder": folder, "synced": now, "source": "Google Drive API",
                       "files": files}, fh, indent=2, ensure_ascii=False)
        print(f"[{slug}] {len(files)} files")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
