import logging
import hashlib
import os

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .model.signup_request import *
from utilitys.db.dbinstance import db_instance
from utilitys.email.email_utils import EmailUtils

api = APIRouter(prefix="/signup")

user_collection=os.getenv("USER_COLLECTION")
CONTENT_COLLECTION= os.getenv("CONTENT_COLLECTION")

@api.get("/verifydomain")
def verify_domain(domain:str):
    return not db_instance.find({"domain":domain}, user_collection) is None

@api.post("/register")
def register_user(data: SignupRequest):
    logging.debug(f'Signup request received: {data}')
    if verify_domain(data.domain[0]):
        return JSONResponse(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            content={"message": "Domain already exists"},
        )
    if db_instance.find(query={"email":data.email}, collection=user_collection) is None:
        # Initialize account settings if not provided
        if data.accountSettings is None:
            data.accountSettings = AccountSettings(isVerified=False, isBlocked=False,MFAEnabled=False, MFAConfigs=[])

        # Hash the password with SHA-512
        hashed_password = hashlib.sha512(data.password.encode('utf-8')).hexdigest()

        # Prepare user data for DB (example dict)
        user_data = {
            "firstName": data.firstName,
            "lastName": data.lastName,
            "domain": data.domain,
            "email": data.email,
            "password": hashed_password,
            "accountSettings": data.accountSettings.dict()
        }
        db_instance.save(user_data,user_collection,"email")
        new_content={"domain":data.domain[0]}
        db_instance.save(new_content,CONTENT_COLLECTION,"domain")
        email_util=EmailUtils()
        if email_util.generate_otp(data.email):
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "User registered successfully"},
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Something Went Wrong"},
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            content={"message": "Account already exists"},
        )
@api.get("/resendotp")
def resend_otp(email:str):
    data= db_instance.find(query={"email":email}, collection=user_collection)
    if data:
        email_util = EmailUtils()
        email_util.generate_otp(data["email"])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Email Sent"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"message": "Account Not Found"},
        )
@api.post("/verify")
def verify(data:OTPRequest):
    util=EmailUtils()
    if util.validate_otp(otp=data.OTP,email=data.email):
        data=db_instance.find({"email":data.email},user_collection)
        data["accountSettings"]["isVerified"]=True
        db_instance.save(data,user_collection)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Verified successfully"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid Otp"},
        )