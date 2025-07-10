from fastapi import FastAPI
import uvicorn, logging, os
from routers.user.main import route as user_route
import logging
from initialisation import initialisation
from routers.content.main import route as content_route
from routers.content.main import ai_route

initialisation()

CONTEXT_PATH= os.getenv("CONTEXT_PATH")

app = FastAPI(title="Analytics API", version="1.0",
              docs_url=f'{CONTEXT_PATH}/documentation',
              redoc_url = None,
              openapi_url = f'{CONTEXT_PATH}/openapi.json'
)

app.include_router(user_route, prefix=f'{CONTEXT_PATH}/api/v1')

app.include_router(content_route, prefix=f'{CONTEXT_PATH}/api/v1')
app.include_router(ai_route, prefix=f'{CONTEXT_PATH}/api/v1')

@app.get(f'{CONTEXT_PATH}/ping',tags=["Ping"])
def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    logging.info(f'Running FastAPI app on port {os.getenv("PORT",80)}')
    uvicorn.run(app,host="0.0.0.0",port=int(os.getenv("PORT",80)))