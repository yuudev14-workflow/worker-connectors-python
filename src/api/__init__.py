from fastapi import APIRouter
from src.api import celery

routes = APIRouter()


routes.include_router(celery.router)