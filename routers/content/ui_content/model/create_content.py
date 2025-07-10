from pydantic import BaseModel
from typing import Optional

class Request(BaseModel):
    domain: str
    content: dict
