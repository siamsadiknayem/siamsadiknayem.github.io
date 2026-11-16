# content/: everything you edit

This folder holds all of your website's text. The design lives elsewhere, so you can't break the layout from here. The worst a typo can do is stop one build. The Actions tab then shows which file it was.

| To change… | Edit |
|---|---|
| Name, intro, positions, education, email, links, CV switch | `_data/profile.yml` |
| Research summary, methods, next questions | `_data/research.yml` |
| Publications | `_data/publications.yml` |
| Courses | `_data/courses.yml` |
| Lecture titles, order and credits | `_data/materials/<course>.yml` |
| Short news (homepage "Updates") | `_data/news.yml` |
| Leadership · timeline · honours · projects | `_data/leadership.yml` · `timeline.yml` · `honours.yml` · `projects.yml` |
| Articles | new file in `_posts/` (drafts in `_drafts/`) |
| Biography | `_pages/about.md` |
| The intro line under any page title | `lede:` in `_pages/<page>.md` |

**Don't edit:** `_data/drive/`. It is filled automatically from Google Drive.

Photos and the CV PDF go in the top-level `files/` folder, not here.

Full instructions: `CONTENT_GUIDE.md`.
