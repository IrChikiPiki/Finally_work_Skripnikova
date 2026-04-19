import os
import configparser
from pathlib import Path
from typing import Optional


class ConfigManager:
    """Класс для управления конфигурацией"""

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """Загрузка конфигурации из файлов"""
        self._config = configparser.ConfigParser()

        # Загрузка config.ini
        config_path = Path(__file__).parent / "config.ini"
        if config_path.exists():
            self._config.read(config_path, encoding="utf-8")

        # Загрузка .env (для чувствительных данных)
        from dotenv import load_dotenv

        load_dotenv()

    def get(
        self, section: str, key: str, fallback: Optional[str] = None
    ) -> str:
        """Получение значения из конфига"""
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise

    def get_env(
        self, key: str, fallback: Optional[str] = None
    ) -> Optional[str]:
        """Получение значения из переменных окружения"""
        return os.getenv(key, fallback)

    @property
    def ui(self) -> "UISection":
        return UISection(self)

    @property
    def projects(self) -> "ProjectsSection":
        return ProjectsSection(self)

    @property
    def api(self) -> "APISection":
        return APISection(self)


class UISection:
    def __init__(self, config: ConfigManager):
        self._config = config

    @property
    def task_name(self) -> str:
        return self._config.get("ui", "task_name", fallback="Тестовая задача")

    @property
    def performer_name(self) -> str:
        return self._config.get("ui", "performer_name", fallback="Ирина")

    @property
    def performer_short(self) -> str:
        return self._config.get("ui", "performer_short", fallback="Ир")


class ProjectsSection:
    def __init__(self, config: ConfigManager):
        self._config = config

    @property
    def main_project(self) -> str:
        return self._config.get(
            "projects", "main_project", fallback="FINALLY_PROJ"
        )

    @property
    def column_name(self) -> str:
        return self._config.get(
            "projects", "column_name", fallback="SkripnikovaFINAL_2"
        )

    @property
    def board_name(self) -> str:
        return self._config.get(
            "projects", "board_name", fallback="ДОСКА ФИНАЛЬНАЯ"
        )

    @property
    def target_column(self) -> str:
        return self._config.get(
            "projects", "target_column", fallback="SkripnikovaFINAL"
        )


class APISection:
    def __init__(self, config: ConfigManager):
        self._config = config

    @property
    def user_id(self) -> str:
        return self._config.get("api", "user_id", fallback="")


# Глобальный экземпляр
config = ConfigManager()
