from fastapi import APIRouter

from app.routers.user_router import router as user_router 
from app.routers.account_router import router as account_router
from app.services.auth_service import router as auth_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(auth_router)
main_router.include_router(account_router)