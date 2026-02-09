# LLM Prompt Repository
Web app for sharing and browsing LLM prompts for scientific research. Users can add prompts anonymously, browse all prompts, and search/filter by purpose. The app ships with seed prompts from the Wolfram Prompt Repository.

## Live URLs
- Frontend: https://llm-prompt-repository.onrender.com/
- Backend API: https://llm-prompt-backend.onrender.com/api/prompts
- API Docs (Swagger): https://llm-prompt-backend.onrender.com/docs

## Features
- Anonymous prompt submission (no authentication)
- Browse and search prompts
- Purpose-based filtering
- Optional tags and source links
- Seeded example prompts

## Architecture
- **Frontend:** Vue 3 + TypeScript + Vite
- **Backend:** FastAPI + Pydantic
- **Database:** SQLite (for MVP/demo)

## API Endpoints
- `POST /api/prompts` — Create a new prompt
- `GET /api/prompts` — List prompts (optional `q` and `purpose` query params)
- `GET /api/prompts/{id}` — Fetch a single prompt

## Local Development

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
uvicorn backend.main:app --reload
```

Backend runs at `http://localhost:8000`.

### Frontend
```bash
cd frontend
npm install
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

Frontend runs at `http://localhost:5173`.

## Configuration
- Frontend API base URL: `VITE_API_BASE_URL`
- Backend environment: `ENV` (`local` or `production`) for CORS behavior

## Reset to Seeded Data (Local)
To reset the database to seeded prompts:
1. Delete the SQLite DB: `backend/data/prompts.db`
2. Restart the backend (it will recreate the DB and re-seed)

## Tech Stack
- Vue 3, TypeScript, Vite
- FastAPI, Pydantic
- SQLite

## License
MIT


