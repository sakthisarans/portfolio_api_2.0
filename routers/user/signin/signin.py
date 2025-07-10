import logging
import hashlib
import os

from .model.signin_request import *
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from utilitys.db.dbinstance import db_instance
from utilitys.email.email_utils import EmailUtils
from utilitys.auth.jwt_util import create_access_token, create_refresh_token  # updated import

api = APIRouter(prefix="/signin")

user_collection = os.getenv("USER_COLLECTION")

@api.post("/")
def signin(data: SigninRequest):
    user = db_instance.find({"email": data.email}, user_collection)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid credentials"},
        )
    hashed_password = hashlib.sha512(data.password.encode('utf-8')).hexdigest()
    if user["password"] != hashed_password:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid credentials"},
        )
    # Create JWT tokens
    logging.debug(f"data - {user}")
    payload = {"email": user.get("email"),
               "user_id": str(user.get("_id")),
               "firstName":user.get("firstName"),
               "lastName":user.get("lastName"),
               "MFAEnabled": user.get("accountSettings", {}).get("MFAEnabled"),
               "accountStatus": user.get("accountSettings", {}).get("isBlocked")
               }
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        },
    )