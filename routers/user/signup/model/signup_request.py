from pydantic import BaseModel
from typing import Optional

class AccountSettings(BaseModel):
    isVerified: bool = False
    isBlocked: bool = False
    MFAEnabled: bool = False
    MFAConfigs:list = []  # Assuming MFAConfigs is a list, adjust as necessary

class SignupRequest(BaseModel):
    firstName: str
    lastName: str
    domain: list[str]
    email: str
    password: str
    accountSettings: Optional[AccountSettings] = None

class OTPRequest(BaseModel):
    OTP: str
    email: str