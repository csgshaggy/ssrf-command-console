# Developer Guide

## 1. Introduction
The Developer Guide provides a technical deep‑dive into the Operator Console’s architecture, development workflow, and extension model.  
It is intended for contributors, maintainers, and engineers integrating new scanning modes, services, or API routes.

This guide covers:
- Project architecture and module responsibilities
- Development environment setup
- Code conventions and patterns
- Adding new routes, services, and models
- Extending the scanning engine
- Debugging and testing workflows

---

## 2. Development Environment

### 2.1 Requirements
- Python 3.10+
- FastAPI
- Uvicorn
- Docker (optional but recommended)
- SQLite or PostgreSQL
- Node/Yarn (only if modifying dashboard assets)

### 2.2 Recommended Tools
- VS Code or PyCharm
- Ruff or Flake8 for linting
- Black for formatting
- HTTP client (Insomnia, Postman, or VS Code REST Client)
- SQLite browser (if using SQLite)

### 2.3 Environment Setup
git clone <repo-url>
cd operator-console
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2.4 Running the Backend
uvicorn app.main:app --reload

### 3. Code Conventions
3.1 Style
 	Follow PEP 8
• 	Use type hints everywhere
• 	Use dependency injection for services
• 	Keep functions small and single‑purpose
• 	Prefer composition over inheritance
3.2 Naming
• 	Modules: 
• 	Classes: 
• 	Functions: 
• 	Constants: 
• 	Routes: grouped by domain (auth, scans, dashboard, system)
3.3 Logging
Use structured logs via :
• 	Include timestamps
• 	Include request IDs
• 	Include operator context when available
• 	Avoid printing raw exceptions; wrap them
3.4 Error Handling
• 	Use FastAPI  for API errors
• 	Wrap mode execution errors with contextual metadata
• 	Never expose internal stack traces to the client

### 4. Application Architecture
4.1 High-Level Overview
The application is structured around:
• 	Routers (API endpoints)
• 	Core (security, config, middleware)
• 	Models (Pydantic + ORM)
• 	Services (business logic)
• 	Modes (plugin scanning modules)
• 	Utils (shared helpers)
• 	Dashboard (templates + static assets)

4.2 Request Flow
1. 	Request enters FastAPI
2. 	Middleware attaches request ID + session context
3. 	Router receives request
4. 	Router delegates to service layer
5. 	Service performs logic or dispatches a scan mode
6. 	Response is normalized via 
7. 	Logs + audit trail are recorded

4.3 Directory Responsibilities
• 	 → HTTP interface
• 	 → security, config, middleware
• 	 → data structures
• 	 → logic + engines
• 	 → scanning plugins
• 	 → helpers
• 	 → dashboard UI
• 	 → dashboard assets
	
## 5. Adding New API Routes

### 5.1 Create a New Router
Add a file under `app/api/`:
python
from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/")
async def example_root():
    return {"message": "Example route"}

5.2 Register the Router
In app/main.py:
from app.api import example
app.include_router(example.router)
