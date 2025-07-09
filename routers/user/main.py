from fastapi import APIRouter
from .signup.signup import api as signup_route
route = APIRouter(prefix="/user",tags=["User"])

route.include_router(signup_route)