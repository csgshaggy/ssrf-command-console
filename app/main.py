from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Routers
from app.routers import (
    auth,
    logs_api,
    ops,
    health,
    dashboard,
)

# Core middleware + rate limiting
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.rate_limit import limiter, rate_limit_exception_handler
from app.core.ip_allowlist import IPAllowlistMiddleware

import os
import traceback


# ------------------------------------------------------------
# Resolve template + static directories safely
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


def create_app() -> FastAPI:
    app = FastAPI(
        title="SSRF Command Console",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------
    # IP Allowlist
    # ------------------------------------------------------------
    app.add_middleware(IPAllowlistMiddleware)

    # ------------------------------------------------------------
    # Rate Limiting
    # ------------------------------------------------------------
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_middleware(SlowAPIMiddleware)

    # ------------------------------------------------------------
    # Static + Templates
    # ------------------------------------------------------------
    if os.path.isdir(STATIC_DIR):
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    else:
        print(f"[WARN] Static directory not found: {STATIC_DIR}")

    # ------------------------------------------------------------
    # Routers
    # ------------------------------------------------------------
    app.include_router(auth.router)
    app.include_router(health.router)
    app.include_router(logs_api.router)
    app.include_router(ops.router)
    app.include_router(dashboard.router)

    # ------------------------------------------------------------
    # Global Exception Handler (Operator‑Grade)
    # ------------------------------------------------------------
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        error_trace = traceback.format_exc()
        print(f"\n[ERROR] Unhandled exception:\n{error_trace}")

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error": str(exc),
            },
        )

    # ------------------------------------------------------------
    # Root Fallback → dashboard.html
    # ------------------------------------------------------------
    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        try:
            return templates.TemplateResponse("dashboard.html", {"request": request})
        except Exception:
            return HTMLResponse(
                "<h1>Dashboard template missing</h1>",
                status_code=500,
            )

    return app


app = create_app()
