from src.infrastructure.config import settings, ServiceType

if settings.service == ServiceType.TELEGRAM:
    from src.presentation.bot.main import main
elif settings.service == ServiceType.API:
    from src.presentation.api.main import main


__all__ = ["main"]
