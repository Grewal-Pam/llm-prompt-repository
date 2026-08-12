# LLM Prompt Repository - Architecture Documentation

## System Overview

This is a full-stack web application for sharing and browsing LLM prompts for scientific research. The architecture follows a clean 3-tier design with clear separation of concerns.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                    (Browser - Chrome/Firefox)                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                       FRONTEND LAYER                                │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │  Vue 3 Single Page Application (SPA)                      │    │
│  │                                                            │    │
│  │  Components:                                               │    │
│  │  ┌─────────────────┐  ┌──────────────────────┐           │    │
│  │  │   App.vue       │  │ AddPromptForm.vue    │           │    │
│  │  │  - Main layout  │  │  - Form validation   │           │    │
│  │  │  - Prompt list  │  │  - Submit handler    │           │    │
│  │  │  - Search/filter│  │  - Success/error     │           │    │
│  │  └────────┬────────┘  └──────────┬───────────┘           │    │
│  │           │                       │                        │    │
│  │           └───────────┬───────────┘                        │    │
│  │                       │                                    │    │
│  │  ┌────────────────────▼─────────────────────┐            │    │
│  │  │   API Service Layer (api.ts)             │            │    │
│  │  │   - fetchPrompts()                       │            │    │
│  │  │   - createPrompt()                       │            │    │
│  │  │   - Centralized HTTP client              │            │    │
│  │  │   - Environment-based API_BASE           │            │    │
│  │  └────────────────────┬─────────────────────┘            │    │
│  │                       │                                    │    │
│  └───────────────────────┼────────────────────────────────────┘    │
│                          │                                         │
│  Technology Stack:                                                 │
│  - Vue 3.5 (Composition API)                                       │
│  - TypeScript                                                      │
│  - Vite 7.2 (build tool)                                           │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ REST API (JSON)
                             │ GET /api/prompts
                             │ POST /api/prompts
                             │ GET /api/prompts/{id}
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                        BACKEND LAYER                                │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │  API Layer (main.py)                                      │    │
│  │  - FastAPI application                                    │    │
│  │  - CORS middleware                                        │    │
│  │  - Request validation (Pydantic)                          │    │
│  │  - Response serialization                                 │    │
│  │  - Error handling (HTTP exceptions)                       │    │
│  └─────────────────────────┬─────────────────────────────────┘    │
│                            │                                       │
│  ┌─────────────────────────▼───────────────────────────────┐      │
│  │  Models Layer (models.py)                               │      │
│  │  - PromptBase (base schema)                             │      │
│  │  - PromptCreate (input validation)                      │      │
│  │  - PromptRead (output serialization)                    │      │
│  └─────────────────────────┬───────────────────────────────┘      │
│                            │                                       │
│  ┌─────────────────────────▼───────────────────────────────┐      │
│  │  Repository Layer (repository.py)                       │      │
│  │  - create_prompt()                                      │      │
│  │  - get_prompts(q?, purpose?)                            │      │
│  │  - get_prompt_by_id()                                   │      │
│  │  - Business logic                                        │      │
│  │  - Data transformation                                   │      │
│  └─────────────────────────┬───────────────────────────────┘      │
│                            │                                       │
│  ┌─────────────────────────▼───────────────────────────────┐      │
│  │  Database Layer (db.py)                                 │      │
│  │  - get_connection()                                     │      │
│  │  - init_db()                                            │      │
│  │  - Connection management                                │      │
│  │  - Schema initialization                                │      │
│  └─────────────────────────┬───────────────────────────────┘      │
│                            │                                       │
│  Technology Stack:                                                 │
│  - Python 3.9+                                                     │
│  - FastAPI (web framework)                                         │
│  - Pydantic (validation)                                           │
│  - sqlite3 (database driver)                                       │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ SQL Queries
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                         DATA LAYER                                  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │  SQLite Database (prompts.db)                             │    │
│  │                                                            │    │
│  │  Table: prompts                                            │    │
│  │  ┌──────────────────────────────────────────────────┐    │    │
│  │  │ id              INTEGER PRIMARY KEY AUTOINCREMENT│    │    │
│  │  │ title           TEXT NOT NULL                     │    │    │
│  │  │ prompt_text     TEXT NOT NULL                     │    │    │
│  │  │ purpose         TEXT NOT NULL                     │    │    │
│  │  │ tags            TEXT (comma-separated)            │    │    │
│  │  │ source          TEXT                              │    │    │
│  │  │ created_at      TIMESTAMP DEFAULT CURRENT_TIME    │    │    │
│  │  └──────────────────────────────────────────────────┘    │    │
│  │                                                            │    │
│  │  Indexes: (future optimization)                            │    │
│  │  - idx_purpose on purpose                                  │    │
│  │  - idx_created_at on created_at                            │    │
│  └───────────────────────────────────────────────────────────┘    │
│                                                                     │
│  Technology: SQLite 3                                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Creating a Prompt

```
User fills form
    ↓
AddPromptForm validates input
    ↓
Calls createPrompt(payload) from api.ts
    ↓
HTTP POST to ${API_BASE}/api/prompts
    ↓
FastAPI receives request in main.py
    ↓
Pydantic validates with PromptCreate model
    ↓
Calls repository.create_prompt()
    ↓
Repository inserts into SQLite via db.get_connection()
    ↓
Returns PromptRead with id and created_at
    ↓
API returns 201 Created + JSON
    ↓
Frontend receives response
    ↓
Form clears, success message shown
    ↓
promptAdded event emitted
    ↓
App.vue calls loadPrompts()
    ↓
GET /api/prompts
    ↓
Updated list displayed
```

### Browsing Prompts

```
User visits page
    ↓
App.vue mounted hook
    ↓
Calls loadPrompts()
    ↓
api.fetchPrompts() → GET /api/prompts
    ↓
FastAPI receives request
    ↓
Calls repository.get_prompts()
    ↓
SQL: SELECT * FROM prompts
    ↓
Repository maps rows to PromptRead objects
    ↓
API returns 200 OK + JSON array
    ↓
Frontend stores in reactive ref
    ↓
Computed property filteredPrompts applies client-side filters
    ↓
Vue renders prompt cards
```

---

## Design Patterns

### 1. Repository Pattern
**Purpose:** Encapsulate data access logic  
**Location:** `backend/repository.py`  
**Benefits:**
- Decouples business logic from SQL
- Easy to test with mocks
- Can swap databases without touching API

### 2. DTO (Data Transfer Object) Pattern
**Purpose:** Define data contracts  
**Location:** `backend/models.py`  
**Implementation:**
- `PromptCreate` for input validation
- `PromptRead` for output serialization
- Pydantic handles validation automatically

### 3. Service Layer Pattern
**Purpose:** Centralize API communication  
**Location:** `frontend/src/services/api.ts`  
**Benefits:**
- Single source of truth for API calls
- Environment-based configuration
- Easy to mock for testing

### 4. Layered Architecture
**Layers:**
1. Presentation (Vue components)
2. API Service (HTTP client)
3. API Endpoints (FastAPI routes)
4. Business Logic (Repository)
5. Data Access (DB module)

---

## Security Considerations

### Current Implementation
- ✅ Parameterized SQL queries (no injection)
- ✅ CORS configured (environment-specific)
- ✅ Pydantic validation (no malformed data)
- ✅ Vue HTML escaping (XSS prevention)

### Missing (By Design)
- ❌ No authentication (requirement: anonymous)
- ❌ No rate limiting
- ❌ No content moderation

### Production Recommendations
- Add API rate limiting (per IP)
- Implement content filtering
- Add CAPTCHA for form submissions
- Monitor for spam patterns
- Add database backups

---

## Scalability Considerations

### Current Limitations
- SQLite: single-file, limited concurrency
- No pagination: loads all prompts
- Client-side filtering: inefficient at scale

### Migration Path to Scale

**Phase 1: Database**
- Switch to PostgreSQL
- Add connection pooling
- Create indexes on `purpose`, `created_at`

**Phase 2: API**
- Add pagination (`?page=1&limit=20`)
- Move filtering to server-side
- Add caching (Redis)

**Phase 3: Search**
- Full-text search (PostgreSQL or Elasticsearch)
- Vector embeddings for semantic search
- Faceted search interface

**Phase 4: Infrastructure**
- Load balancer
- Multiple API instances
- CDN for static assets
- Background jobs for data ingestion

---

## Testing Strategy

### Backend Tests
```
tests/
├── test_db.py           # Database connection, init
├── test_models.py       # Pydantic validation
├── test_repository.py   # CRUD operations
└── test_api.py          # Endpoint integration
```

### Frontend Tests
```
tests/
├── api.test.ts          # API service
├── AddPromptForm.test.ts  # Form validation
└── App.test.ts          # Component integration
```

---

## Deployment Architecture

### Development
```
localhost:5173 (Vite dev server)
    ↓ CORS
localhost:8000 (FastAPI uvicorn)
    ↓
prompts.db (local file)
```

### Production (Render)
```
CDN (static frontend)
    ↓ HTTPS
API Server (FastAPI)
    ↓
PostgreSQL (managed service)
```

### Environment Variables
- **Frontend:** `VITE_API_BASE_URL`
- **Backend:** `ENV` (local/production)

---

## Technology Choices & Rationale

| Choice | Rationale |
|--------|-----------|
| **Vue 3** | Lightweight, reactive, great TypeScript support |
| **TypeScript** | Type safety, better IDE support, fewer bugs |
| **FastAPI** | Modern, fast, automatic docs, async support |
| **Pydantic** | Runtime validation, serialization, OpenAPI integration |
| **SQLite** | Zero-config, embedded, perfect for MVP/demo |
| **Repository Pattern** | Clean architecture, testable, maintainable |

---

## File Structure

```
llm-prompt-repository/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + routes
│   ├── models.py        # Pydantic schemas
│   ├── repository.py    # Data access layer
│   ├── db.py            # Database connection
│   ├── seed_wolfram.py  # Initial data
│   └── data/
│       └── prompts.db   # SQLite database
├── frontend/
│   ├── src/
│   │   ├── App.vue      # Main component
│   │   ├── main.ts      # Entry point
│   │   ├── components/
│   │   │   └── AddPromptForm.vue
│   │   └── services/
│   │       └── api.ts   # HTTP client
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Maintenance & Evolution

### Easy to Change
- ✅ Swap SQLite for Postgres (change `db.py` only)
- ✅ Add new endpoints (extend `main.py`)
- ✅ Add new fields (update `models.py` + migration)
- ✅ Change UI styling (modify Vue components)

### Requires More Work
- ❌ Add authentication (affects all layers)
- ❌ Add real-time updates (needs WebSockets)
- ❌ Multi-language support (i18n setup)

---

## Performance Characteristics

**Current Performance:**
- Frontend: Static assets, instant load
- API: ~10ms response time (local)
- Database: In-memory for small datasets
- Search: Client-side, negligible latency

**Bottlenecks at Scale:**
- SQLite write concurrency
- Loading all prompts without pagination
- Client-side filtering of large datasets

---

## Conclusion

This architecture balances **simplicity** and **maintainability**. It's production-ready for small-to-medium scale, with a clear path to scale when needed.

The clean separation of concerns makes it:
- ✅ Easy to understand
- ✅ Easy to test
- ✅ Easy to extend
- ✅ Easy to deploy
