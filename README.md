# Siam Sadik Nayem: academic website

Personal academic website: research, publications, teaching and course materials. It is built with Jekyll and hosted free on GitHub Pages.

- **Repository:** github.com/siamsadiknayem/siamsadiknayem.github.io
- **Live site:** https://siamsadiknayem.github.io
- **Updating content:** [CONTENT_GUIDE.md](CONTENT_GUIDE.md)
- **Rules for Claude-assisted maintenance:** [CLAUDE.md](CLAUDE.md)

## Design and content are kept apart

```
siam-academic-website/
│
├── content/                  ← YOUR CONTENT: edit freely
│   ├── _data/                   profile, publications, courses, news, research …
│   │   ├── materials/           lecture titles & order for each course
│   │   └── drive/               (automatic) file lists from Google Drive
│   ├── _posts/                  published articles (Markdown)
│   ├── _drafts/                 unpublished drafts
│   ├── _pages/                  page text: about.md (biography), research.md …
│   └── _albums/                 gallery albums: one file per album
│       └── courses/             one small file per course page
│
├── files/                    ← YOUR UPLOADS: photo, CV PDF, article images, gallery
│   ├── images/
│   └── gallery/<album>/
│
├── _layouts/  _includes/     ← DESIGN: page structure (built once)
├── assets/css/main.css       ← DESIGN: colours, fonts, spacing
├── _config.yml               ← SITE SETTINGS (address, plugins)
├── scripts/sync_drive.py     ← reads your Google Drive course folders
└── .github/workflows/        ← builds and publishes the site automatically
```

Blog posts, course resources, publications, the CV and news live **only** in `content/` and `files/`. Adding or changing them never requires touching the design folders.

Tested: an article, a news item and a CV PDF were added by changing only `content/` and `files/`, and all three appeared on the rebuilt site.

## How publishing works

Every push to `main` runs `.github/workflows/build-and-deploy.yml`, which:

1. reads your Google Drive course folders and the Website Gallery folder (photo albums),
2. builds the site with Jekyll, and
3. publishes it to GitHub Pages.

It also runs every 6 hours, so Drive changes appear automatically. To run it immediately: **Actions → Build and deploy site → Run workflow**.

## Test locally before publishing

You need Ruby on your computer.

**On a Mac, one-time setup:**

```bash
brew install ruby                          # needs Homebrew: https://brew.sh
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
gem install bundler
```

**Every time, in this folder:**

```bash
bundle install                 # first time only; installs the GitHub Pages versions
bundle exec jekyll serve       # builds and serves the site
# open http://localhost:4000 ; edits to content/ reload automatically
bundle exec jekyll serve --drafts   # also shows articles in content/_drafts/
```

**What to check before publishing:**

- the homepage, each menu item and both course pages;
- one VIEW ↗ link on a course page;
- the page in your browser's phone view (in Chrome: View → Developer → Toggle device toolbar).

A successful local build is not the same as a working live site. After publishing, always open `https://siamsadiknayem.github.io` and check it there too.
