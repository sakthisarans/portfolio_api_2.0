from fastapi import APIRouter
from .signup.signup import api as signup_route
from .signin.signin import api as signin_route
from .token.token import api as token_route
route = APIRouter(prefix="/user")

route.include_router(signup_route,tags=['SignUp'])
route.include_router(signin_route,tags=["SignIn"])
route.include_router(token_route,tags=["Token"])