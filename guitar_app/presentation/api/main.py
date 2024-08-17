import logging

import uvicorn
from fastapi import FastAPI

from guitar_app.config import get_settings, setup_logging
from guitar_app.infrastructure.db.main import build_sessions, create_engine

from .controllers import setup_controllers
from .di import setup_di

logger = logging.getLogger(__name__)


def build_app() -> FastAPI:
    app = FastAPI()
    settings = get_settings()

    setup_logging()
    db_engine = create_engine(settings.DB_URL)

    setup_di(app, build_sessions(db_engine))
    setup_controllers(app.router)

    logger.info("app prepared")
    return app


if __name__ == "__main__":
    uvicorn.run(
        app="guitar_app.presentation.api.main:build_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
