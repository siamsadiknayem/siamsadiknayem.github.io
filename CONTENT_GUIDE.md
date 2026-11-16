# Content guide

This guide covers how to keep your website up to date. Every example uses the real files in this repository.

**Your content lives in two folders, and you only ever edit those:**

| Folder | What's in it |
|---|---|
| `content/` | All text: profile, publications, courses, lecture titles, news, articles (`_posts/`), and page wording (`_pages/`) |
| `files/` | Uploads: your photo, CV PDF, and article images |

Everything else (`_layouts/`, `_includes/`, `assets/css/`, `_config.yml`) is the design. It was built once and doesn't need changing when you add content.

**Editing on GitHub without installing anything:**

1. Open the file on github.com.
2. Click the ✏️ pencil icon.
3. Make your change.
4. Click **Commit changes**.

The site rebuilds itself in about 2 minutes. Check progress in the **Actions** tab.

> **YAML tips**
> - Indentation matters. Use spaces, never tabs.
> - If text contains a colon followed by a space (`: `), wrap it in double quotes: `title: "Phase: an introduction"`.
> - If a build fails, the Actions tab shows a red ✗. The usual cause is a YAML indentation slip in the file you last edited.

---

## Contents

1. [Publish a new article](#1-publish-a-new-article)
2. [Add a short news item](#2-add-a-short-news-item)
3. [Add lecture slides to a course](#3-add-lecture-slides-to-a-course-google-drive)
4. [Give a lecture a proper title, or reorder lectures](#4-give-a-lecture-a-proper-title-or-reorder-lectures)
5. [Replace or update a lecture file](#5-replace-or-update-a-lecture-file)
6. [Hide a file from the website](#6-hide-a-file-from-the-website)
7. [Add a new course](#7-add-a-new-course)
8. [Replace your CV](#8-replace-your-cv)
9. [Add a publication](#9-add-a-publication)
10. [Add a project](#10-add-a-project)
11. [Update your biography and homepage text](#11-update-your-biography-and-homepage-text)
12. [Change your profile photo](#12-change-your-profile-photo)
13. [First-time setup: publish on GitHub Pages](#13-first-time-setup-publish-on-github-pages)
14. [First-time setup: connect Google Drive](#14-first-time-setup-connect-google-drive)
15. [Add a custom domain later](#15-add-a-custom-domain-later)
16. [Add a photo album to the gallery](#16-add-a-photo-album-to-the-gallery)
17. [Edit "My Vision"](#17-edit-my-vision)
18. [How the email links work](#18-how-the-email-links-work)

---

## 1. Publish a new article

Articles appear under **Updates**, newest first. Each article is one Markdown file in `content/_posts/`.

**File name:** `YYYY-MM-DD-short-title.md`, for example `content/_posts/2026-12-05-teaching-fourier-series.md`.

**Contents:**

```markdown
---
title: "What I learned teaching Fourier series this semester"
category: Teaching Experiences
tags: [teaching, Fourier series]
excerpt: One or two sentences shown in the list of updates.
---

Write the article here in plain Markdown.

## A heading

- a bullet point
- another one

[A link](https://example.com) · **bold** · *italic*

![Describe the image for screen readers](/files/images/posts/fourier-board.jpg)
```

**Categories you can use:** Academic Updates, Teaching Experiences, Research Progress, Projects, Seminars and Workshops, Publications, Technical Articles, Professional Reflections.

**Dates:** an article dated in the future stays hidden until that day. This is handy for scheduling. If an article doesn't appear, check the date in the file name.

**Images:** put them in `files/images/posts/`. Keep them under about 300 KB; resizing to 1600 px wide is plenty.

**Drafts:** files in `content/_drafts/` are never published. Two drafts are waiting there for you to review:

- `acs-omega-glucose-article.md`
- `signals-dsp-materials-seu.md`

To publish one:

1. Read the note at the top of the file and fill in what it asks for.
2. Move the file into `content/_posts/`.
3. Add the date to the file name.

---

## 2. Add a short news item

For one-line news, such as a talk, an award or a new role, you don't need an article. Open `content/_data/news.yml` and add a line **at the top**:

```yaml
- date: Dec 2026
  text: Invited talk on non-invasive glucose sensing at XYZ University.
```

The homepage shows the newest three items. The Updates page shows all of them.

---

## 3. Add lecture slides to a course (Google Drive)

Your course pages read their file lists straight from Google Drive. They currently use two folders:

| Course | Drive folder |
|---|---|
| EEE 237 | "Signal": `12MrH8YEd6o_FpMLfXLqkxFwHZ9qcA9_F` |
| EEE 325 | "DSP": `1EiPscwm8ALYOc_ZI1viMxrOFKzEhqSPA` |

**To add a lecture:**

1. Upload the file (PDF, PowerPoint, Google Slides or Google Doc) into the course's Drive folder.
2. Wait. Within 6 hours it appears on the course page under **Recently added**, titled from the file name.
3. If you want it live immediately, go to GitHub → **Actions** → **Build and deploy site** → **Run workflow**.

Name files clearly, for example `Lecture 14 - IIR filters.pdf`. The name is used as the title until you set a better one (section 4).

**Sub-folders:** a sub-folder inside the course folder, such as "Lab manuals", is included too. Its name shows under each file.

**Sharing:** the course folder must be shared as **Anyone with the link → Viewer**. Check this in Drive with Share → General access. Files inherit it from the folder.

**Never put these in a course folder:** marks, attendance, student names, exam papers you don't want public, or anything confidential to the university. Everything in the folder is public.

---

## 4. Give a lecture a proper title, or reorder lectures

Open `content/_data/materials/eee325.yml` (or `eee237.yml`). Lectures are grouped into parts. Each lecture is one line:

```yaml
groups:
  - title: FIR filters and LTI systems
    items:
      - { id: 1ikG7A1Hymsq0krokQzkdh1lYmuoAckV9, label: Lecture 13, title: Frequency response of FIR filters, type: slides, credit: dspfirst }
```

To add your new Lecture 14, add a line under the right part, or start a new part:

```yaml
  - title: IIR filters
    items:
      - { id: PASTE_FILE_ID_HERE, label: Lecture 14, title: IIR filter design, type: slides, credit: dspfirst }
```

**Finding a file's id:** open the file in Drive. In the address bar, the id is the long code between `/d/` and `/view`. For example, in `drive.google.com/file/d/1ikG7A1Hymsq0krokQzkdh1lYmuoAckV9/view` the id is `1ikG7A1Hymsq0krokQzkdh1lYmuoAckV9`.

**Fields:**

- `label`: shown on the left, for example `Lecture 14`, `Lab 2` or `Tutorial`.
- `title`: what students see.
- `note` (optional): a one-line description.
- `credit` (optional): which entry under `credits:` at the top of the file applies.

**Reading lists** use the `reading:` section at the bottom of the same file.

**Changing order:** move the lines around. The page follows the order in the file.

**Crediting material by other authors:** add a credit once under `credits:` and refer to it by name. The credits print at the bottom of the course page.

```yaml
credits:
  oppenheim: Slides adapted from Signals and Systems, A. V. Oppenheim and A. S. Willsky.
```

---

## 5. Replace or update a lecture file

**To keep the same link (recommended):**

1. In Drive, right-click the file → **File information** → **Manage versions** → **Upload new version**.
2. Upload the new file.

The file id stays the same, so the website entry keeps its title and position. Only the "updated" date changes.

**If you upload a new file instead and delete the old one:** the old entry disappears from the site, and the new file appears under **Recently added** until you give it an entry (section 4).

---

## 6. Hide a file from the website

To hide a file without removing it from Drive, add its id under `hidden:` in the course's materials file:

```yaml
hidden: [1qOy1vZVZPR5I25tTi9sgsCwcFY_amUfU]
```

---

## 7. Add a new course

**Step 1:** add the course to `content/_data/courses.yml`, copying an existing entry:

```yaml
- slug: eee326
  code: EEE 326
  title: Digital Signal Processing I Laboratory
  institution: Southeast University
  department: Department of EEE
  programme: B.Sc. in EEE
  kind: Lab
  role: Adjunct Lecturer
  page: true
  drive_folder: PASTE_FOLDER_ID
  summary: One or two sentences describing the course.   # optional
  syllabus:                                               # optional
    - heading: Experiments
      text: Short description from the curriculum.
```

The folder id is the code after `/folders/` in the folder's share link.

Optional fields, each shown on the course page only when present: `credits`, `summary`, `methods` (teaching methods), `assessment`, `syllabus` (list of heading + text), `syllabus_note`, `plan` (weekly lesson plan: `week`, `lectures`, `topics`, `exam`), `books` (list of text) and `sites` (list of `label` + `url`). CSE 1301, 1303, 2203 and 3205 are filled in from the course outlines, so copy one of them as an example.

**Step 2:** create `content/_pages/courses/eee326.md` with only this. Anything you write below the second `---` appears on the course page as extra notes for students.

```markdown
---
layout: course
course: eee326
title: EEE 326 Digital Signal Processing I Laboratory
permalink: /courses/eee326/
description: Lab manuals and materials for EEE 326 at Southeast University.
---
```

**Step 3:** create `content/_data/materials/eee326.yml` with:

```yaml
credits: {}
groups: []
reading: []
hidden: []
```

All files in the folder will then appear under "Recently added". Give them titles later as in section 4.

**A course without materials:** set `page: false` and leave out `drive_folder`. It appears in the course lists without a link.

---

## 8. Replace your CV

1. Export a **public** version of your CV as PDF, without your phone number, home address or referees' contact details.
2. Name it exactly `Siam_Sadik_Nayem_CV.pdf` and upload it into the `files/` folder on GitHub: **Add file → Upload files**. Replace the old one if there is one.
3. In `content/_data/profile.yml`, set:

   ```yaml
   cv_available: true
   cv_updated: "Dec 2026"
   ```

The CV page and homepage button then link to the PDF. To update it later, upload a new file with the same name.

---

## 9. Add a publication

Open `content/_data/publications.yml` and add an entry at the top, newest first. Write your name exactly as `S. S. Nayem` so it appears in bold.

```yaml
- id: nayem2027wearable
  status: published
  type: journal
  tag: JOURNAL
  year: 2027
  title: Full title of the paper
  authors: S. S. Nayem, A. Coauthor, B. Coauthor
  venue: Journal Name
  details: 12(3), 100–110
  doi: 10.xxxx/xxxxx
  summary: One plain-language sentence about what the paper shows.
  bibtex: |
    @article{nayem2027wearable,
      title = {...},
      author = {Nayem, Siam Sadik and ...},
      journal = {...}, year = {2027}, doi = {10.xxxx/xxxxx}
    }
```

- **Submitted papers:** use `status: under_review` with only `title` and `venue`. They show labelled "Under review" and never as published.
- **When a paper is accepted:** change the status and fill in the rest.

---

## 10. Add a project

Add an entry to `content/_data/projects.yml`:

```yaml
- title: Wearable NIR sensor prototype
  category: research        # research | engineering | team
  context: Bangladesh University
  period: "2027"
  problem: What problem it addresses.
  contribution: What you did.
  tools: [Python, Arduino]
```

---

## 11. Update your biography and homepage text

- **Homepage sentence, intro paragraph, positions, education, PhD line:** `content/_data/profile.yml`.
- **Research summary, methods and future questions:** `content/_data/research.yml`.
- **Full biography:** `content/_pages/about.md`. Everything below the second `---` is the biography, in plain Markdown (**bold**, *italic*).
- **Page introductions** (the line under each page title): the `lede:` line in that page's file in `content/_pages/`.
- **Timeline on the About page:** `content/_data/timeline.yml`.
- **Changing jobs:** update `positions:` in `profile.yml` and `timeline.yml`, and add a news item.

---

## 12. Change your profile photo

1. Prepare a square photo, about 640 × 640 px and under 100 KB.
2. Upload it to `files/images/` as `siam.jpg`, replacing the old one.

The same photo is used on the homepage, the About page and in link previews.

To use a different file name, change `photo:` in `content/_data/profile.yml`.

---

## 13. First-time setup: publish on GitHub Pages

You do this once.

**Your repository:** [github.com/siamsadiknayem/siamsadiknayem.github.io](https://github.com/siamsadiknayem/siamsadiknayem.github.io)

**Your address:** **https://siamsadiknayem.github.io**. The repository name matches the username, so GitHub serves it at the main address. This is already set in `_config.yml`.

1. **Upload the site:**
   - Open the repository. It's currently empty.
   - Click **uploading an existing file**.
   - Drag in **everything inside** the `siam-academic-website` folder. That includes the hidden `.github` folder: press Cmd+Shift+. in Finder to show hidden folders.
   - Don't upload `_site/`. It's the built copy for local preview, and GitHub builds its own.
   - Click **Commit changes**.
2. **Turn on Pages:** go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
3. **Add the Google key:** see section 14. Course materials and the gallery need it.
4. **Watch the first build:** open the **Actions** tab. A green ✓ means the site is live. The first time takes 2–5 minutes.
5. **Test the public site** at https://siamsadiknayem.github.io:
   - Open each menu item.
   - Open both course pages and click one VIEW ↗ link. Try it in a private window, so you see what signed-out visitors see.
   - Click "Download CV".
   - Click an email link.
   - Check on your phone.

A successful build on its own does not prove the site works. Always check the live address.

---

## 14. First-time setup: connect Google Drive

Without this step, the course pages show the file lists saved on 16 Nov 2026 and don't update, and the Drive gallery stays empty. With it, they follow your Drive folders automatically.

You need a free Google API key. It only lets the website read files you have already shared publicly.

1. Go to <https://console.cloud.google.com/> and sign in.
2. Create a project: click the project picker → **New project**, name it "website", then **Create**.
3. Go to **APIs & Services → Library**, search for **Google Drive API**, and click **Enable**.
4. Go to **APIs & Services → Credentials → Create credentials → API key**. Copy the key.
5. Restrict the key:
   - Click the key.
   - Under **API restrictions**, choose **Restrict key** → **Google Drive API**.
   - Click **Save**.
6. In GitHub, go to your repository → **Settings → Secrets and variables → Actions → New repository secret**.
   - Name: `GOOGLE_API_KEY`
   - Secret: paste the key
   - Click **Add secret**.
7. Go to **Actions → Build and deploy site → Run workflow**. In the log, the "Sync course materials" step should report something like `[eee325] 15 files`.

> Keep the key private. Never paste it into a file in the repository, an email or a chat, including a chat with Claude. GitHub Secrets is the only place it belongs.

**If the sync step says it can't read a folder:**

- Check that the folder is shared as **Anyone with the link → Viewer**.
- Your Southeast University Google account may block public sharing. If it does, move the course folders to your personal Google Drive and share them from there. Then update `drive_folder:` in `content/_data/courses.yml`.

**How often it updates:** every 6 hours, on every change you push, and whenever you click **Run workflow**. GitHub pauses scheduled runs in repositories with no activity for 60 days. Any commit, or one click of **Run workflow**, restarts them.

---

## 15. Add a custom domain later

1. Buy the domain.
2. In `_config.yml`, set `url: "https://yourdomain.com"`.
3. In GitHub, go to **Settings → Pages → Custom domain**, enter the domain and save.
4. At your domain registrar, add the DNS records GitHub shows you.

You don't need to change anything else. All internal links adjust automatically.

---

## 16. Add a photo album to the gallery

Albums appear on the homepage, newest three first, and on the Gallery page at `/gallery/`. The homepage section stays hidden until the first album exists.

### From your iPhone (Google Drive app), recommended

Your gallery folder is **Website Gallery** in your Google Drive (siamsadik202@gmail.com). Every folder inside it is one album.

**One-time setup:**
1. In Drive, open **Website Gallery** → **Share** → **General access** → **Anyone with the link** → **Viewer**.
2. Make sure the `GOOGLE_API_KEY` secret is set (section 14). It's the same key the course pages use.

**To make an album on your iPhone:**
1. Open the **Google Drive** app → **Website Gallery** → **+** → **Folder**.
2. Name the folder with the date first, then the title, for example `2024-10-12 IEEE ProCon 2024`. The date sets the album's order and date. `2025-03 Chapter launch` also works.
3. Open the folder → **+** → **Upload** → choose photos from your Photos library. iPhone HEIC photos are fine; they're converted automatically.
4. **Captions:** rename a photo to its caption (⋯ → Rename), for example `Opening session`. Photos keeping camera names like `IMG_4021` simply have no caption.
   - **Order:** put a number in front, such as `01 Opening session`, `02 With the committee`. The number isn't shown.
   - **Cover:** name one photo `cover`. Otherwise the first photo is the cover.
5. **Album description (optional):** add a Google Doc named `about` to the folder and write a sentence or two in it.

The album appears on the website at the next automatic update, within 6 hours. To publish straight away: GitHub → **Actions** → **Build and deploy site** → **Run workflow**. This also works from the GitHub iPhone app.

**What the website does with your photos:**
- turns them the right way up;
- converts HEIC to JPEG;
- shrinks them to 1600 px;
- **removes hidden GPS location data**.

The originals in Drive are not changed.

**Change or remove things:**
- **Rename or delete** photos in Drive; the site follows at the next update.
- **Hide an album** without deleting it: add its folder name under `hidden:` in `content/_data/gallery.yml`.
- **Add a location or a longer description:** use `albums:` in the same file.

### From GitHub (alternative)

You can also add an album by hand:
1. Upload photos to `files/gallery/<album-name>/`.
2. Copy `content/_albums/_TEMPLATE.md` to `content/_albums/<album-name>.md` and fill in the title, date and captions.

Both kinds of album appear together, sorted by date.

**Privacy:** only upload photos you have the right to share. Get permission before posting photos where students can be clearly identified. Everything in Website Gallery becomes public.

---

## 17. Edit "My Vision"

The text is in `content/_data/vision.yml`.

- Each paragraph starts with `- >-` on its own line, followed by the text, indented.
- To add a paragraph, copy one whole block.
- To hide the section, delete all the paragraphs.

---

## 18. How the email links work

Clicking your email address anywhere on the site opens **Gmail's "New message" window** with your address already filled in. On the CV and course pages, the subject line is filled in too.

Visitors who use Gmail in their browser get a ready-to-send message. Visitors without a Gmail account are asked to sign in to Google. Your address is always shown as text next to the link, so they can copy it instead.

The address comes from `email:` in `content/_data/profile.yml`.

