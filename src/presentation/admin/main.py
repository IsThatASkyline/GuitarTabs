from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.admin import setup_admin_models


def create_admin_instance(app: FastAPI, engine: AsyncEngine):
    admin = Admin(app, engine)
    setup_admin_models(admin)
