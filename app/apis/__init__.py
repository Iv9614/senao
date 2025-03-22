from fastapi import APIRouter

from app.apis.routes import urls

route = APIRouter()

route.include_router(urls.router)
