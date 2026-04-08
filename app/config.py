from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IdeaSecretary"
    default_locale: str = "en"
    data_dir: Path = Path("data")
    media_dir_name: str = "media"
    media_trash_dir_name: str = "media_trash"
    backup_dir_name: str = "backups"
    sqlite_file_name: str = "idea_secretary.db"
    backup_every_operations: int = 20
    backup_keep_latest: int = 5
    openai_api_key: str = ""
    openai_base_url: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / self.sqlite_file_name

    @property
    def media_dir(self) -> Path:
        return self.data_dir / self.media_dir_name

    @property
    def media_trash_dir(self) -> Path:
        return self.data_dir / self.media_trash_dir_name

    @property
    def backup_dir(self) -> Path:
        return self.data_dir / self.backup_dir_name


settings = Settings()
