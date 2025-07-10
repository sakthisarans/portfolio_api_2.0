from utilitys.auth.jwt_util import verify_access_token

from fastapi import APIRouter, Depends
from .ui_content.content_control import api as content_route
from .ui_content.content_control import get_route
from .ai.knowledge import api as ai_router
route = APIRouter(prefix="/content",tags=["Content"])


ai_route = APIRouter(prefix="/ai",tags=["Ai"])

route.include_router(content_route,dependencies=[Depends(verify_access_token)])
route.include_router(get_route)

ai_route.include_router(ai_router,dependencies=[Depends(verify_access_token)])
