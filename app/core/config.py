# app/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # ----------------------------------------------------------------------
    # Core application settings
    # ----------------------------------------------------------------------
    app_name: str = "SSRF Command Console Backend"
    environment: str = "development"

    # ----------------------------------------------------------------------
    # Security / JWT
    # ----------------------------------------------------------------------
    SECRET_KEY: str | None = None     # Required by your backend
    jwt_secret: str | None = None     # Required by validator

    # ----------------------------------------------------------------------
    # OAuth (optional for now)
    # ----------------------------------------------------------------------
    oauth_client_id: str | None = None
    oauth_client_secret: str | None = None
    oauth_auth_url: str | None = None
    oauth_token_url: str | None = None
    oauth_redirect_uri: str | None = None

    # ----------------------------------------------------------------------
    # Pydantic v2 config
    # ----------------------------------------------------------------------
    model_config = {
        "extra": "allow",          # Prevents "extra inputs not permitted"
        "env_file": ".env",        # Optional
        "env_file_encoding": "utf-8",
    }


# Global settings instance
settings = Settings()
