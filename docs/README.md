# Operator Console — README
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)
![Status](https://img.shields.io/badge/Status-Active-success)

## Overview
The Operator Console is a modular, extensible, forensic‑grade automation toolkit designed for secure SSRF testing, environment validation, dashboard integration, and operator‑friendly workflows.  
It provides a unified interface for scanning, analysis, authentication, and operational lifecycle management.

This project is built for:
- Security engineers
- SOC analysts
- IAM / Support Engineering workflows
- Red team operators
- Developers building modular scanning or automation tools

The architecture emphasizes:
- Clean separation of concerns
- Plugin‑style extensibility
- Crash‑resistant execution
- Operator‑friendly UX
- Forensic clarity and auditability

---

## Key Features

### Modular Scanning Engine
- Plugin‑based scanning modes
- Drop‑in modules under `modes/`
- Unified dispatcher for consistent execution
- Pattern‑driven enumeration and anomaly detection

### Authentication & Security
- Google OAuth integration
- JWT issuance and validation
- Session cookies (secure, HttpOnly)
- Refresh tokens
- RBAC (role‑based access control)
- DB‑backed session persistence

### Dashboard Integration
- Static + dynamic dashboard rendering
- Role‑based UI
- Operator‑grade status panels
- Integrated logs, snapshots, and diff viewers

### Environment Validation System
- Preflight checks
- Baseline snapshots
- Regression detection
- Timestamped audit trails
- Plugin‑driven validation modules

### Operational Toolkit
- Health checks
- Log viewers
- Service lifecycle management
- TUI menus (optional)
- Automated recovery scripts

---

## Project Structure

project/
│
├── app/                                  # Core FastAPI application (modular, operator‑grade)
│   ├── api/                              # All HTTP routers (auth, scans, dashboard, system)
│   │   ├── auth.py                       # OAuth, JWT, session mgmt
│   │   ├── scans.py                      # Scan dispatch + mode execution
│   │   ├── dashboard.py                  # Dynamic dashboard routes
│   │   └── system.py                     # Health checks, service info, diagnostics
│   │
│   ├── core/                             # Security + foundational infrastructure
│   │   ├── config.py                     # Settings, env loading, global config
│   │   ├── security.py                   # JWT, cookies, RBAC, token utilities
│   │   ├── middleware.py                 # Logging, request tracing, session middleware
│   │   └── database.py                   # DB engine + session management
│   │
│   ├── models/                           # Pydantic + ORM models
│   │   ├── user.py                       # User, roles, permissions
│   │   ├── session.py                    # Session persistence
│   │   └── scan.py                       # Scan requests, results, metadata
│   │
│   ├── services/                         # Business logic + operational engines
│   │   ├── dispatcher.py                 # Mode loader + unified execution pipeline
│   │   ├── validators.py                 # Preflight + environment validation engine
│   │   ├── snapshots.py                  # Baseline snapshots + regression diffing
│   │   └── logging_service.py            # Structured logging + audit trail helpers
│   │
│   ├── utils/                            # Shared helpers (forensic‑grade utilities)
│   │   ├── patterns.py                   # Pattern matching + anomaly detection
│   │   ├── decorators.py                 # Timing, tracing, error‑wrapping decorators
│   │   ├── filetools.py                  # Safe file ops, path mgmt, sandboxing
│   │   └── response.py                   # Unified API response formatting
│   │
│   └── main.py                           # FastAPI entrypoint (mounts routers, static, templates)
│
├── modes/                                # Plugin‑style scanning modules (auto‑discovered)
│   ├── mode_template.py                  # Base class + required interface
│   ├── ssrf_basic.py                     # Example mode: basic SSRF probing
│   ├── ssrf_advanced.py                  # Example mode: advanced SSRF heuristics
│   └── ...                               # Additional operator‑defined modes
│
├── scripts/                              # Operational lifecycle + maintenance scripts
│   ├── setup.sh                          # Environment bootstrap + dependency checks
│   ├── restart_backend.sh                # Safe backend restart with validation
│   └── validate_env.py                   # Preflight checks, regression detection, audit logs
│
├── static/                               # Dashboard static assets (CSS, JS, images)
├── templates/                            # Jinja2 templates for dynamic dashboard rendering
│
├── docker/                               # Dockerfile, compose stack, runtime configs
│
├── tests/                                # Unit + integration tests (API, modes, validators)
│
└── DOCUMENTATION.md                      # Combined documentation (optional)
## Installation

### 1. Clone the repository
git clone <repo-url>
cd operator-console

### 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Environment variables
Creat .env:
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
JWT_SECRET=...
DATABASE_URL=sqlite:///./operator.db

### 5. Running the Backend
	### Development mode
	uvicorn app.main:app --reload

	### Production mode
	uvicorn app.main:app --host 0.0.0.0 --port 8000

### Docker Deployment
Build - docker build -t operator-console .
Run - docker run -p 8000:8000 operator-console
Compose - docker compose up --build

### Adding a New Scanning Mode
1. Copy modes/mode_template.py 
2. Rename it (e.g.,modes/ssrf_custom.py )
3. Implement:
	a. metadata
	b. validate_config
	c. execute
4. The  dispatcher auto-detects it at runtime.

### Authentication Flow
1. 	User logs in via Google OAuth
2. 	Backend receives Google token
3. 	Backend issues:
• 	Access token (JWT)
• 	Refresh token
• 	Secure session cookie
4. 	RBAC determines dashboard visibility
5. 	Sessions persist in DB

### Troubleshooting
Backend returns 404 for all routes
• 	Router not mounted
• 	Wrong import path after refactor
• 	Missing  in  or submodules
Dashboard not rendering
• 	Static/templates not mounted
• 	Wrong template directory path
• 	Missing Jinja2 dependency
OAuth failing
• 	Redirect URI mismatch
• 	Missing environment variables
• 	Clock skew issues

### Contributing
1. 	Fork the repo
2. 	Create a feature branch
3. 	Submit a PR with:
 		Clear description
 		Test coverage
 		Updated documentation
### License

MIT License

Copyright (c) 2026 Charles Roberts

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
