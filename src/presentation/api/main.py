import uvicorn
from fastapi import FastAPI

from guitar_app.src.config import get_settings
from guitar_app.src.infrastructure.db.main import build_sessions, create_engine
from guitar_app.src.presentation.admin.main import create_admin_instance

from .controllers import setup_controllers
from .di import setup_di


def build_app() -> FastAPI:
    app = FastAPI()
    settings = get_settings()
    db_engine = create_engine(settings.DB_URL)

    setup_di(app, build_sessions(db_engine))

    create_admin_instance(
        app,
        db_engine,
    )

    setup_controllers(app.router)

    return app


if __name__ == "__main__":
    uvicorn.run(
        app="src.presentation.api.main:build_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )