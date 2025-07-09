
from pydantic import BaseModel
from typing import Optional

class SigninRequest(BaseModel):
    password: str
    email: str