---
# HOW TO MAKE AN ALBUM (files starting with "_" are never published)
# 1. Upload your photos into a new folder:   files/gallery/my-album-name/
#    Use simple file names: 01.jpg, 02.jpg ... (no spaces).
# 2. Copy this file to content/_albums/my-album-name.md (same name as the folder,
#    without the underscore) and fill it in. The album's address becomes
#    /gallery/my-album-name/
# 3. Commit. The album appears on the homepage and the Gallery page.

title: IEEE ProCon 2024
date: 2024-10-12                 # YYYY-MM-DD; newest albums are shown first
location: KUET, Khulna           # optional
description: One or two sentences about the event, shown under the title.
cover: /files/gallery/my-album-name/01.jpg   # optional; first photo if left out
photos:
  - file: /files/gallery/my-album-name/01.jpg
    caption: Short description of this photo.
  - file: /files/gallery/my-album-name/02.jpg
    caption: Another description.
---
Optional: a longer paragraph about the album, in Markdown.
