from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Telegram
    bot_token: str

    # RSS
    rss_refresh_minutes: int = 20
    rss_last_days: int = 3

    # DB
    db_path: str = "/app/data/db.sqlite"

    # Manual run mode
    manual_run: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
