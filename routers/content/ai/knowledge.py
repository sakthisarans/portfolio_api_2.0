import logging
import hashlib
import os

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from utilitys.db.dbinstance import db_instance
from dotenv import load_dotenv
load_dotenv()

CONTENT_COLLECTION= os.getenv("AI_COLLECTION")

api = APIRouter()

@api.post("/createkb")
def createkb():
    print()