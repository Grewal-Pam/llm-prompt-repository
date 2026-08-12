# LLM Prompt Repository
## Anonymous Web App for Scientific Research

**Parminder Grewal**  
February 2026

---

## Problem & Goal

### The Challenge
- Social scientists need a simple way to share reusable LLM prompts
- No central repository for research-focused prompts
- High friction in current solutions

### The Solution
✅ Add prompts anonymously  
✅ Browse and search all prompts  
✅ Seeded with examples from Wolfram Prompt Repository  
✅ Simple, fast, focused

---

## Architecture Overview

### 3-Tier Architecture

**Frontend Layer**
- Vue 3 with Composition API
- TypeScript for type safety
- Vite for fast development

**Backend Layer**
- FastAPI (Python)
- Pydantic validation
- Repository pattern

**Data Layer**
- SQLite database
- Simple, embedded, zero-config

---

## System Architecture Diagram

```
┌─────────────────────────────────────────┐
│          FRONTEND (Vue 3)               │
│  ┌─────────────────────────────────┐   │
│  │  App.vue                        │   │
│  │  - Search & Filter UI           │   │
│  │  - Prompt List Display          │   │
│  │                                 │   │
│  │  AddPromptForm.vue              │   │
│  │  - Form Validation              │   │
│  │  - Submit Handler               │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│  ┌──────────▼──────────────────────┐   │
│  │  API Service (api.ts)           │   │
│  │  - fetchPrompts()               │   │
│  │  - createPrompt()               │   │
│  └──────────┬──────────────────────┘   │
└─────────────┼───────────────────────────┘
              │ HTTP REST
              │ (JSON)
┌─────────────▼───────────────────────────┐
│        BACKEND (FastAPI)                │
│  ┌─────────────────────────────────┐   │
│  │  main.py (API Layer)            │   │
│  │  POST   /api/prompts            │   │
│  │  GET    /api/prompts            │   │
│  │  GET    /api/prompts/{id}       │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│  ┌──────────▼──────────────────────┐   │
│  │  repository.py                  │   │
│  │  - create_prompt()              │   │
│  │  - get_prompts()                │   │
│  │  - get_prompt_by_id()           │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│  ┌──────────▼──────────────────────┐   │
│  │  db.py                          │   │
│  │  - get_connection()             │   │
│  │  - init_db()                    │   │
│  └──────────┬──────────────────────┘   │
└─────────────┼───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│        DATABASE (SQLite)                │
│                                         │
│  Table: prompts                         │
│  - id, title, prompt_text               │
│  - purpose, tags, source                │
│  - created_at                           │
└─────────────────────────────────────────┘
```

---

## Data Model

### Prompt Schema

**Required Fields:**
- `title` — Short descriptive name
- `prompt_text` — The actual prompt content
- `purpose` — Category/use case

**Optional Fields:**
- `tags` — Array of keywords
- `source` — Origin/attribution URL

**System Fields:**
- `id` — Auto-generated
- `created_at` — Timestamp

---

## API Endpoints

### RESTful Design

**Create Prompt**
```
POST /api/prompts
Body: { title, prompt_text, purpose, tags?, source? }
Response: 201 Created + full prompt object
```

**List Prompts**
```
GET /api/prompts?q=keyword&purpose=category
Response: 200 OK + array of prompts
```

**Get Single Prompt**
```
GET /api/prompts/{id}
Response: 200 OK + prompt object
```

---

## Key Design Decisions

### 1. Repository Pattern
- Separates data access from business logic
- Makes testing easier
- Allows DB swap without touching API

### 2. Pydantic Validation
- Type-safe request/response
- Automatic validation errors
- OpenAPI docs generation

### 3. Anonymous by Design
- No authentication required
- Lower barrier to contribution
- Simplifies architecture

### 4. Seeded Data
- Instant value on first load
- Examples from Wolfram Prompt Repository
- Demonstrates use cases

---

## Demo Walkthrough

### Live Application Flow

1. **Landing Page** — View seeded prompts
2. **Search** — Filter by keyword
3. **Filter** — Select purpose category
4. **Add Prompt** — Fill form & submit
5. **Instant Update** — New prompt appears

---

## Technical Highlights

### Frontend
- ✅ Reactive state with Vue refs
- ✅ Computed properties for filtering
- ✅ Client-side search for speed
- ✅ Environment-based API config

### Backend
- ✅ Parameterized SQL queries (injection-safe)
- ✅ CORS configured for dev/prod
- ✅ Startup events for DB init
- ✅ HTTP status codes follow REST standards

---

## Limitations & Trade-offs

### Current Limitations
❌ SQLite not ideal for high scale  
❌ Basic search (SQL `LIKE`)  
❌ No authentication or moderation  
❌ No pagination (loads all prompts)  

### Why These Choices?
✅ Rapid development  
✅ Zero deployment complexity  
✅ Sufficient for MVP/demo  
✅ Meets requirements exactly  

---

## Future Enhancements

### If I Had More Time

**Phase 1 — Scale**
- Migrate to PostgreSQL
- Add pagination (20 prompts/page)
- Server-side search

**Phase 2 — Quality**
- Full-text search (Postgres or ElasticSearch)
- Vector search for semantic matching
- Tag autocomplete

**Phase 3 — Safety**
- Rate limiting
- Content moderation
- Spam detection
- Optional auth for edit/delete

---

## Why This Matters

### Research Impact
- 📚 Promotes reproducible research workflows
- 🤝 Encourages community knowledge sharing
- ⚡ Reduces time spent crafting prompts
- 🔧 Simple, extendable foundation

### Technical Value
- Clean architecture patterns
- Production-ready structure
- Easy to understand and modify
- Well-suited for academic use cases

---

## Questions?

**Demo:** https://llm-prompt-repository.onrender.com/
**Code:** https://github.com/Grewal-Pam/llm-prompt-repository  
**API:** https://llm-prompt-backend.onrender.com/docs

Thank you!

---

## Appendix: Tech Stack

**Frontend**
- Vue 3.5
- TypeScript
- Vite 7.2

**Backend**
- Python 3.9+
- FastAPI
- Pydantic
- SQLite3

**Deployment**
- Render
- Environment variables for config
