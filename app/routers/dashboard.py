from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Any, Dict, List

from app.services.dispatcher_service import dispatcher_service

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# In-memory state
HISTORY: List[Dict[str, Any]] = []
FAVORITES: List[str] = []


# ------------------------------------------------------------
# UI Routes (Dynamic Jinja2 Templates)
# ------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
async def dashboard_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "username": "Operator",   # placeholder until auth integration
            "roles": ["admin"],       # placeholder until auth integration
        }
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "username": "Operator",
            "roles": ["admin"],
        }
    )


# ------------------------------------------------------------
# Modes
# ------------------------------------------------------------
@router.get("/api/modes")
def api_list_modes():
    try:
        return dispatcher_service.list_modes()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/api/run")
async def api_run(payload: Dict[str, Any]):
    mode = payload.get("mode")
    target = payload.get("target")
    options = payload.get("options") or {}

    if not mode or not target:
        return JSONResponse(
            status_code=400,
            content={"error": "mode and target are required"},
        )

    try:
        result = dispatcher_service.run_mode(mode, target, options)
        HISTORY.append(
            {
                "mode": mode,
                "target": target,
                "options": options,
                "result": result,
            }
        )
        return {"mode": mode, "target": target, "options": options, "result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ------------------------------------------------------------
# History
# ------------------------------------------------------------
@router.get("/api/history")
def api_get_history():
    return HISTORY


@router.delete("/api/history")
def api_clear_history():
    HISTORY.clear()
    return {"status": "cleared"}


# ------------------------------------------------------------
# Favorites
# ------------------------------------------------------------
@router.get("/api/favorites")
def api_get_favorites():
    return FAVORITES


@router.post("/api/favorites/{mode_name}")
def api_add_favorite(mode_name: str):
    if mode_name not in FAVORITES:
        FAVORITES.append(mode_name)
    return {"status": "ok", "favorites": FAVORITES}


@router.delete("/api/favorites/{mode_name}")
def api_remove_favorite(mode_name: str):
    if mode_name in FAVORITES:
        FAVORITES.remove(mode_name)
    return {"status": "ok", "favorites": FAVORITES}


# ------------------------------------------------------------
# Diagnostics
# ------------------------------------------------------------
@router.get("/api/diagnostics")
def api_diagnostics():
    try:
        modes = dispatcher_service.list_modes()
        modes_error = None
    except Exception as e:
        modes = []
        modes_error = str(e)

    return {
        "cwd": str(Path.cwd()),
        "base_dir": str(BASE_DIR),
        "static_dir_exists": STATIC_DIR.exists(),
        "templates_dir_exists": TEMPLATES_DIR.exists(),
        "modes_count": len(modes),
        "modes": modes,
        "modes_error": modes_error,
    }


# ------------------------------------------------------------
# Structure Check
# ------------------------------------------------------------
@router.get("/api/structure-check")
def api_structure_check():
    return {
        "base_dir": str(BASE_DIR),
        "paths": {
            "dispatcher.py": (BASE_DIR / "dispatcher.py").exists(),
            "modes/": (BASE_DIR / "modes").exists(),
            "console/": (BASE_DIR / "console").exists(),
            "static/": STATIC_DIR.exists(),
            "templates/": TEMPLATES_DIR.exists(),
            "requirements.txt": (BASE_DIR / "requirements.txt").exists(),
        },
    }


# ------------------------------------------------------------
# Themes
# ------------------------------------------------------------
THEMES = ["default", "dark", "high-contrast"]


@router.get("/api/themes")
def api_list_themes():
    return THEMES


@router.post("/api/themes/{theme_name}")
def api_apply_theme(theme_name: str):
    if theme_name not in THEMES:
        return JSONResponse(
            status_code=400,
            content={"error": f"Unknown theme '{theme_name}'"},
        )
    return {"status": "ok", "applied": theme_name}


# ------------------------------------------------------------
# Health
# ------------------------------------------------------------
@router.get("/healthz")
def healthz():
    return {"status": "ok"}
