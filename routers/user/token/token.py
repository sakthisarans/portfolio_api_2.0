import logging
import hashlib
import os

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from utilitys.auth.jwt_util import verify_access_token, generate_access_token_from_refresh

api = APIRouter(prefix="/token")

@api.get("/verify")
def get_token(current_user: dict = Depends(verify_access_token)):
    return JSONResponse(status_code=status.HTTP_200_OK,content={'message':"Ok"})

@api.post("/refresh")
def refresh(token: dict ):

    new_token=generate_access_token_from_refresh(token.get("token"))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": new_token,
            "token_type": "Bearer"
        },
    )

@api.post("/signout")
def signout(token:dict):
    print()
