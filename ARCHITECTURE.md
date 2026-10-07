# Polar Science Hub - Architecture & Design Specification

## 1. System Overview

**Polar Science Hub** is an integrated knowledge repository, public science outreach portal, and media dissemination platform tailored for polar scientific research (Arctic, Antarctic, and the Third Pole/Himalayas).

The application is built on a modular Flask 3 application factory architecture, adhering strictly to:
- **WCAG 2.1 AA** accessibility compliance (high contrast ratios, keyboard navigation, skip links, ARIA landmarks, visible focus rings).
- **Role-Based Access Control (RBAC)** across 4 user tiers: Reader, Contributor, Editor, and Admin.
- **Scientific Metadata Standards**: Dublin Core 15-element compliance for all archival and research records.
- **Explainable & Grounded AI**: Clear `AI-GENERATED` badging, grounding references to repository primary sources, and mandatory **Human-in-the-Loop (HITL) Fact-Checking Gates** before scheduling or publication.
- **Data Integrity**: Transparent `DEMO DATA` badging on sample fixtures.

---

## 2. Technology Stack

| Layer | Component | Technology / Implementation |
|---|---|---|
| **Backend Framework** | Application Core | Python 3.11+, Flask 3.0.x |
| **ORM & Database** | Data Persistence | Flask-SQLAlchemy 3.1+ (SQLite with FTS5 for local/test; PostgreSQL 15+ ready) |
| **Authentication & RBAC** | User Management | Flask-Login 0.6+, Werkzeug security (PBKDF2 SHA-256) |
| **Security & Forms** | Validation & Defense | Flask-WTF, WTForms, CSRFProtect, Bleach (HTML sanitization), Flask-Limiter |
| **Search Engine** | Information Retrieval | Multi-entity weighted lexical & tag matching with SQLite FTS5 extension |
| **AI Content Engine** | Generation & Summarization | Provider-agnostic `LLMService` (supports OpenAI, Anthropic, Gemini, with deterministic grounded local mock) |
| **Frontend Templates** | Server-Side Rendering | Jinja2 with semantic HTML5 and accessible layout hierarchy |
| **Styling** | Visual Design System | Custom Vanilla CSS (Design Tokens, Glassmorphism, Dual Polar Dark/Light Mode, Zero CSS Frameworks) |
| **Client-Side Scripting** | Interactive Components | Vanilla ES6+ JavaScript (Modules, Fetch API, debounce controllers) |
| **Data Visualization** | Scientific Plotting | Chart.js 4.4.x (Time series, correlation charts, responsive dark/light theme aware) |
| **Geospatial Mapping** | Polar Geospatial Visuals | Leaflet 1.9.4 with custom Arctic/Antarctic/Global coordinate bounds and CartoDB Dark/Positron tiles |

---

## 3. High-Level System Architecture

```mermaid
graph TD
    Client[Web Browser / Client]
    
    subgraph SecurityLayer [Security & Gateway Layer]
        CSP[Content Security Policy & Security Headers]
        Limiter[Flask-Limiter Rate Limiter]
        CSRF[CSRF Protection]
        AuthGuard[RBAC Route Guards: Reader, Contributor, Editor, Admin]
    end

    subgraph AppCore [Polar Science Hub Application Factory]
        AppInit[Flask App Factory: create_app]
        
        subgraph Blueprints [Core Blueprints]
            MainBP[main: Portal Landing, Search, Static]
            AuthBP[auth: Authentication & Profiles]
            KnowledgeBP[knowledge: Research & Expeditions]
            ResearchBP[research: Publications & Datasets]
            MediaBP[media: Video, Audio, Photo Archive]
            EducationBP[education: Lessons, Quizzes, Glossary]
            StudioBP[studio: AI Dissemination & Fact-Check]
            AdminBP[admin: Submissions, Audit, Analytics]
            APIBP[api: Autocomplete, Geospatial, CSV Preview]
        end

        subgraph ServiceLayer [Domain Services]
            SearchSvc[SearchService: Multi-Entity FTS5 Engine]
            LLMSvc[LLMService: Grounded Scientific Generator]
            StorageSvc[LocalStorageService: Sanitized File Storage]
            AdapterSvc[SocialAdapters: Platform Formatting]
        end
    end

    subgraph DataPersistence [Persistence Layer]
        SQLiteDB[(SQLite / PostgreSQL Database)]
        Uploads[(Sanitized File Store / Uploads)]
        AuditDB[(Audit Logs & Search Logs)]
    end

    Client --> CSP
    CSP --> Limiter
    Limiter --> CSRF
    CSRF --> AuthGuard
    AuthGuard --> Blueprints
    Blueprints --> ServiceLayer
    ServiceLayer --> DataPersistence
```

---

## 4. Entity-Relationship (ER) Data Model

```mermaid
erDiagram
    USER ||--o{ SUBMISSION : submits
    USER ||--o{ AUDIT_LOG : triggers
    USER ||--o{ BOOKMARK : saves
    USER ||--o{ RECENTLY_VIEWED : views
    USER ||--o{ QUIZ_ATTEMPT : attempts
    USER ||--o{ SOCIAL_CONTENT : authors
    USER ||--o{ CONTENT_REVIEW : reviews
    USER ||--o{ DATASET_ACCESS_REQUEST : requests

    CATEGORY ||--o{ ARTICLE : categorizes
    CATEGORY ||--o{ RESEARCH_RESOURCE : categorizes
    CATEGORY ||--o{ MEDIA_ITEM : categorizes
    CATEGORY ||--o{ LESSON : categorizes

    LOCATION ||--o{ ARTICLE : referenced_at
    LOCATION ||--o{ EXPEDITION : staged_at
    LOCATION ||--o{ RESEARCH_RESOURCE : observed_at
    LOCATION ||--o{ MEDIA_ITEM : captured_at

    EXPEDITION ||--o{ ARTICLE : yields
    EXPEDITION ||--o{ RESEARCH_RESOURCE : collects
    EXPEDITION ||--o{ MEDIA_ITEM : documents

    SCIENTIST ||--o{ RESEARCH_RESOURCE : authored_by
    SCIENTIST ||--o{ EXPEDITION : participated_in

    DATASET ||--o{ DATASET_ACCESS_REQUEST : evaluated_under

    QUIZ ||--|{ QUIZ_QUESTION : contains
    QUIZ ||--o{ QUIZ_ATTEMPT : evaluated_in

    SOCIAL_CONTENT ||--o{ CONTENT_REVIEW : verified_by

    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role
        string full_name
        string institution
        boolean is_active
        datetime created_at
    }

    CATEGORY {
        int id PK
        string name UK
        string slug UK
        string description
        string domain
    }

    LOCATION {
        int id PK
        string name
        string region
        float latitude
        float longitude
        string description
    }

    EXPEDITION {
        int id PK
        string title
        string slug UK
        string region
        date start_date
        date end_date
        string lead_agency
        text summary
        string status
        boolean is_demo
    }

    ARTICLE {
        int id PK
        string title
        string slug UK
        text summary
        text content
        int category_id FK
        int location_id FK
        int expedition_id FK
        string status
        boolean is_demo
        string dc_creator
        string dc_coverage
    }

    RESEARCH_RESOURCE {
        int id PK
        string title
        string slug UK
        string resource_type
        string doi UK
        text abstract
        string file_path
        int scientist_id FK
        int category_id FK
        boolean is_demo
    }

    DATASET {
        int id PK
        string title
        string slug UK
        string temporal_coverage
        string spatial_coverage
        string file_format
        string file_path
        string access_level
        boolean is_demo
    }

    MEDIA_ITEM {
        int id PK
        string title
        string slug UK
        string media_type
        string file_path
        string alt_text
        string license
        boolean is_demo
    }

    QUIZ {
        int id PK
        string title
        string slug UK
        string topic
        string difficulty
    }

    QUIZ_QUESTION {
        int id PK
        int quiz_id FK
        text question_text
        string option_a
        string option_b
        string option_c
        string option_d
        string correct_option
        text explanation
    }

    SOCIAL_CONTENT {
        int id PK
        string title
        string content_type
        string target_platform
        text body
        string status
        boolean is_ai_generated
        string ai_model
        int source_entity_id
        string source_entity_type
    }

    CONTENT_REVIEW {
        int id PK
        int content_id FK
        int reviewer_id FK
        boolean facts_checked
        boolean names_checked
        boolean dates_checked
        boolean sources_cited
        string decision
        text comments
    }

    SUBMISSION {
        int id PK
        int user_id FK
        string entity_type
        int content_id
        string status
        datetime submitted_at
        datetime decided_at
    }

    AUDIT_LOG {
        int id PK
        int user_id FK
        string action
        string target_type
        int target_id
        string ip_address
        datetime timestamp
    }
```

---

## 5. Key Workflows & Sequence Diagrams

### 5.1 Content Studio: AI Dissemination & Fact-Checking Gate

The Content Studio implements a strict **Human-in-the-Loop (HITL)** architecture. No AI-generated piece can be scheduled or broadcast to public channels without passing the 4-point verification checklist.

```mermaid
sequenceDiagram
    autonumber
    actor Editor as Editor / Comm Team
    participant Studio as Studio Blueprint
    participant LLM as Grounded LLM Service
    participant Repo as Knowledge Repository (DB)
    participant ReviewGate as Fact-Checking Gate
    participant Adapter as Social Adapters

    Editor->>Studio: Selects Source Record (e.g., Article / Research Dataset)
    Editor->>Studio: Selects Target Channels (Twitter/X, LinkedIn, Newsletter)
    Studio->>Repo: Fetch Dublin Core metadata & primary text
    Repo-->>Studio: Verified ground truth text & citations
    Studio->>LLM: Generate summary with prompt & strict source bounds
    LLM-->>Studio: Grounded Draft (Tagged is_ai_generated=True)
    Studio->>Repo: Save SocialContent(status='draft', is_ai_generated=True)
    
    Note over Editor,ReviewGate: Human-in-the-Loop Fact-Checking Gate
    Editor->>ReviewGate: Access /studio/review/{id}
    ReviewGate-->>Editor: Present Side-by-Side: Original Source vs AI Draft
    Editor->>ReviewGate: Verify Checklist (facts_checked, names_checked, dates_checked, sources_cited)
    
    alt Verification Incomplete
        Editor->>ReviewGate: Submit with unverified checks
        ReviewGate-->>Editor: Validation Error: All checks required for approval
    else Verification Approved
        Editor->>ReviewGate: Submit All Checked + decision='approved'
        ReviewGate->>Repo: Update ContentReview & SocialContent(status='approved')
        Editor->>Studio: Schedule for Publication (/studio/schedule/{id})
        Studio->>Adapter: Format payload for target platform schema
        Adapter-->>Studio: Formatted platform payload
        Studio->>Repo: Update SocialContent(status='scheduled')
    end
```

---

### 5.2 Contributor Submission & Editorial Moderation Workflow

```mermaid
stateDiagram-v2
    [*] --> Draft : Contributor initiates resource submission
    Draft --> Submitted : Contributor uploads file & Dublin Core metadata
    
    state Submitted {
        [*] --> QueuedInAdmin
        QueuedInAdmin --> UnderReview : Editor/Admin opens submission
    }

    UnderReview --> Rejected : Fails scientific standards or metadata incomplete
    Rejected --> Draft : Contributor revises based on feedback
    
    UnderReview --> Approved : Editorial standards met
    Approved --> Published : Entity status set to 'published'
    
    Published --> [*] : Discoverable via Public Search & Maps
```

---

### 5.3 Unified Search & Autocomplete Retrieval

```mermaid
sequenceDiagram
    autonumber
    actor User as Portal Visitor
    participant Frontend as Search Bar (main.js)
    participant API as /api/search-suggest
    participant SearchEngine as SearchService
    participant DB as SQLite FTS5 / SQL Tables

    User->>Frontend: Types search query ("Himadri glacier")
    Frontend->>Frontend: Debounce 250ms
    Frontend->>API: GET /api/search-suggest?q=Himadri
    API->>SearchEngine: suggest("Himadri")
    SearchEngine->>DB: Query Article, Expedition, Dataset titles & tags
    DB-->>SearchEngine: Matching titles & types
    SearchEngine-->>API: Suggestion JSON (title, url, category)
    API-->>Frontend: Display accessible live dropdown
    
    User->>Frontend: Press Enter / Click Search
    Frontend->>SearchEngine: GET /search?q=Himadri+glacier
    SearchEngine->>DB: Execute multi-entity scored search
    DB-->>SearchEngine: Ranked result objects
    SearchEngine->>DB: Log query into SearchLog
    SearchEngine-->>User: Render /search results with facet filters & demo badges
```

---

### 5.4 Interactive Polar Map Controller Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as Portal Visitor
    participant View as /map/ Web Page
    participant JS as map.js (Leaflet)
    participant GeoAPI as /api/locations

    User->>View: Navigates to Interactive Polar Map
    View->>JS: Initialize Leaflet Map Container
    JS->>GeoAPI: Fetch all active research stations, camps, & sites
    GeoAPI-->>JS: GeoJSON / Coordinate array with metadata
    JS->>JS: Render custom colored SVG markers (Stations, Camps, Marine)
    
    User->>JS: Click "Arctic Region" Filter Button
    JS->>JS: flyTo([78.9, 11.9], zoom=4) - Svalbard / Ny-Ålesund Focus
    
    User->>JS: Click "Antarctica Region" Filter Button
    JS->>JS: flyTo([-70.7, 11.7], zoom=3) - Maitri / Bharati Focus
    
    User->>JS: Clicks Map Marker
    JS->>JS: Open Accessible Popup with coordinates, description, and direct link to related expeditions
```

---

## 6. Security & Compliance Architecture

1. **Authentication & Password Storage**:
   - Werkzeug PBKDF2 with SHA-256 and salted hashing.
   - Session cookies configured with `HttpOnly=True`, `SameSite=Lax`, and `Secure=True` in production.
2. **Defensive Web Headers**:
   - Strict `Content-Security-Policy` restricting script execution to authorized domains (Leaflet CDN, Chart.js CDN, local static).
   - `X-Frame-Options: DENY` preventing clickjacking.
   - `X-Content-Type-Options: nosniff`.
   - `Referrer-Policy: strict-origin-when-cross-origin`.
3. **Role-Based Access Control (RBAC)**:
   - Route decorators: `@login_required`, `@role_required(['editor', 'admin'])`, `@admin_required`.
   - Dynamic UI rendering hiding privileged administrative tools from unauthorized roles.
4. **Audit Trail**:
   - Sensitive actions (`login`, `logout`, `submission_create`, `submission_decide`, `content_approved`, `content_rejected`, `dataset_request`) logged to immutable `AuditLog` table with user ID, action timestamp, and client IP.
5. **Sanitized File Ingestion**:
   - `LocalStorageService` enforces strict MIME/extension allowlists (`.pdf`, `.csv`, `.jpg`, `.png`, `.mp4`).
   - Filenames are randomized with UUIDs to eliminate path traversal vulnerabilities.

---

## 7. Migration & Scalability Path

### 7.1 Transition to PostgreSQL
The ORM model layer uses standard SQLAlchemy types compatible with PostgreSQL:
1. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://polar_user:polar_secure_pass@localhost:5432/polar_science_hub
   ```
2. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```
3. Run initialization:
   ```bash
   python run.py init-db
   python run.py seed-demo
   ```

### 7.2 Containerization & Production Deployment
- **WSGI Server**: Gunicorn with 4 gevent/async workers.
- **Reverse Proxy**: NGINX handling TLS termination, gzip compression, and static asset caching.
- **Background Worker**: Celery or APScheduler running scheduled publishing queues and automated dataset validation tasks.
