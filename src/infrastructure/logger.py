import logging
from logging.config import dictConfig
from src.infrastructure.config import settings


def setup_logging() -> None:
    settings.logs.dir_path.mkdir(parents=True, exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "DEBUG",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": f"{settings.logs.dir_path}/app.log",
                    "formatter": "default",
                    "level": "INFO",
                    "encoding": "utf-8",
                },
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
            },
            "loggers": {
                "aiogram": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
                "app": {  # <-- Добавляем этот логгер
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
            },
        }
    )


logger_app = logging.getLogger("app")
