from fastapi import APIRouter

from app.routers.user_router import router as user_router 



main_router = APIRouter()

main_router.include_router(user_router)