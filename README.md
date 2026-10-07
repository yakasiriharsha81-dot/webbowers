# Polar Science Hub
**Integrated Polar Science Outreach, Knowledge Repository & Media Dissemination Portal**

![Demo Data Badge](https://img.shields.io/badge/Data-DEMO_DATA_ONLY-amber)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask_3-cyan)
![Database](https://img.shields.io/badge/Database-SQLite_FTS5-lightgrey)
![Accessibility](https://img.shields.io/badge/Accessibility-WCAG_2.1_AA-green)

---

## 1. Project Overview

The **Polar Science Hub** is a full-stack scientific platform serving researchers, educators, students, policymakers, and the public. It fulfills three critical responsibilities:

1. **Knowledge Repository:** Long-term archival stewardship of expedition reports, scientific datasets, Dublin Core-aligned publications, high-resolution media, and institutional activities with rich metadata and full-text search.
2. **Outreach & Education:** Accessible educational resources, plain-language lessons with reading level toggles (Simple vs. Detailed), interactive quizzes with instant feedback, polar glossary, news, event calendars, and an interactive polar map with Arctic/Antarctic/Global projection views.
3. **Media Dissemination (Content Studio):** AI-assisted, human-approved translation of dense repository records into multi-platform outreach: plain-language web summaries, social posts (X/Twitter, LinkedIn, Instagram, Facebook), press blurbs, and newsletters—gated by a mandatory human fact-checking review before scheduled publishing.

---

## 2. Non-Negotiable Standards & Ethical Rules

- **Zero Fake Facts Presented as Genuine:** All seed records, scientific parameters, personnel names, and research papers are synthetic and visibly labeled with a persistent **`DEMO DATA`** badge (`is_demo = true` in database). Well-known geographic regions and stations are used strictly in a generic educational capacity.
- **AI Transparency:** Every AI-generated output is labeled **`AI-GENERATED`**, stores references to the source records used, and cannot be published without human approval via an editor fact-check verification gate.
- **Accessibility First:** Engineered to conform with **WCAG 2.1 Level AA** standards (minimum 4.5:1 color contrast, full keyboard navigation, screen reader skip links, descriptive alt texts, and audio/video transcripts).
- **Security First:** Argon2/scrypt password hashing, session cookie protections (`HttpOnly`, `SameSite=Lax`), CSRF tokens on all state-changing forms, input sanitization, randomized upload filenames, and comprehensive `AuditLog` tracking.

---

## 3. Fixed Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11+, Flask 3, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-Limiter |
| **Database** | SQLite with FTS5 search (PostgreSQL-ready schema) |
| **Frontend** | Jinja2 templates, HTML5 semantic elements, Vanilla CSS (CSS custom properties, CSS Grid/Flexbox), Vanilla JavaScript (ES6+). Zero heavy frontend frameworks. |
| **Geospatial Map** | Leaflet.js with OpenStreetMap tiles and view toggles (Arctic / Antarctic / Global) |
| **Data Plotting** | Chart.js for dataset time-series preview and admin analytics |
| **File Storage** | Local `uploads/` folder abstracted behind `StorageService` interface |
| **AI Outreach** | Provider-agnostic `LLMService` (default deterministic mock mode, live API provider ready) |

---

## 4. Quick Start & Setup

### Prerequisites
- Python 3.11+
- Git

### Installation Steps

1. **Clone and enter repository:**
   ```bash
   cd polar_science_hub
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize configuration:**
   ```bash
   copy .env.example .env   # Windows
   # or
   cp .env.example .env     # macOS / Linux
   ```

5. **Load Demo Database:**
   ```bash
   flask seed-demo
   ```
   *This automatically creates all tables and populates realistic demo content (users, categories, expeditions, datasets, CSV sample files, quizzes, media, news, events, scientists, and glossary terms).*

6. **Run Development Server:**
   ```bash
   python run.py
   # or
   flask run
   ```
   Visit `http://127.0.0.1:5000` in your web browser.

---

## 5. Documented Demo Logins

> ⚠️ **Note:** These credentials are for local development and functional evaluation only. Change secrets and passwords in production.

| Role | Email | Password | Access Privileges |
|---|---|---|---|
| **Admin** | `admin@polarscience.org` | `PolarAdmin2026!` | Full administrative console, user role management, category editor, submission decisions, analytics, audit log viewer |
| **Editor** | `editor@polarscience.org` | `PolarEditor2026!` | Content Studio, fact-check review gate, social dissemination queue, submission approvals |
| **Contributor** | `researcher1@polarscience.org` | `PolarResearch2026!` | Authoring drafts, submitting articles, editing rejected submissions |
| **Regular User** | `student1@university.edu` | `PolarUser2026!` | Bookmarking, recently viewed history, taking interactive quizzes, saving quiz scores |

---

## 6. Modules & Features

- **Home (`/`):** Hero search with debounced autocomplete, category quick-chips, portal stats counters, featured expedition, latest research, news grid, and media spotlights.
- **Knowledge Repository (`/knowledge`):** Curated articles categorized by polar topic, sorting (newest/most viewed/A–Z), pagination, and bookmarking.
- **Research Library (`/research`):** Dublin Core metadata tables, citation copy button, dataset archive with in-browser CSV table previews, dynamic Chart.js time-series plots, and restricted dataset access request modal.
- **Field Expeditions (`/expeditions`):** Comprehensive story pages linking objectives, timeline activities, lead scientists, team members, datasets, and field media.
- **Media Center (`/media`):** Filterable gallery of photographs, field videos, hydrophone audio recordings, and infographics with transcripts, credits, and licensing.
- **Education Hub (`/education`):** Dual-mode lessons (Simple vs. Detailed reading toggle), interactive quizzes with instant card feedback and explanations, and searchable A–Z glossary.
- **Interactive Polar Map (`/map`):** Leaflet map with Arctic (80°N), Antarctic (80°S), and Global focus views, layer filters (stations, expeditions, landmarks), and synchronized keyboard-accessible listing.
- **AI Assistant (`/assistant`):** Grounded Q&A answering strictly based on retrieved repository records with transparent citations and AI-generated labels.
- **Content Studio (`/studio`):** AI outreach generator for web summaries, social variants (X/LinkedIn/Instagram/Facebook), newsletters, and press blurbs with mandatory fact-checking gate and scheduling queue.
- **Admin Console (`/admin`):** Dashboard metrics, review queue with approve/reject notes, analytics with Chart.js charts and CSV export, user role management, and audit log viewer.

---

## 7. Running Tests

To run the automated pytest test suite:
```bash
python -m pytest -v
```
All tests verify authentication, role-based access control, search ranking, and submission lifecycles.

---

## 8. Switching to PostgreSQL in Production

The SQLAlchemy models are designed without database-specific dialect locks. To migrate to PostgreSQL:
1. Install `psycopg2-binary`:
   ```bash
   pip install psycopg2-binary
   ```
2. Update `DATABASE_URL` in your `.env`:
   ```env
   DATABASE_URL=postgresql://polar_user:polar_pass@localhost:5432/polar_science_db
   ```
3. Run migrations or initialization:
   ```bash
   flask db upgrade
   # or
   flask seed-demo
   ```

---

## 9. Known Limitations

- **Social Media Publishing:** Currently operates via simulated channel adapters (`TwitterAdapter`, `LinkedInAdapter`, etc.) that log formatted payloads and provide CSV exports of the queue. Real social API credentials can be plugged in without restructuring.
- **Polar Map Projections:** The map utilizes standard OpenStreetMap Web Mercator tiles with specialized high-latitude camera centering (80°N / 80°S) for broad compatibility. Proj4Leaflet polar stereographic EPSG:3031/3413 custom tile servers can be configured in `map.js`.
