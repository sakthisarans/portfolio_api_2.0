import logging
import hashlib
import os

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from .model.create_content import Request
from utilitys.db.dbinstance import db_instance
from dotenv import load_dotenv
load_dotenv()

CONTENT_COLLECTION= os.getenv("CONTENT_COLLECTION")

api = APIRouter()
get_route = APIRouter()

@api.put("/update")
@api.post("/create")
def create_content(data:Request):
    db_instance.save(data,CONTENT_COLLECTION,"domain")

@get_route.get("/getcontent")
def get_content(domain:str):
    logging.debug(f"Query - {domain}")
    content = db_instance.find({"domain":domain},CONTENT_COLLECTION)
    logging.debug(f"Data - {content}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )