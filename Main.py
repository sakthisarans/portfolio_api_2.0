from fastapi import FastAPI
import uvicorn, logging, os
import logging
from initialisation import initialisation

CONTEXT_PATH= os.getenv("CONTEXT_PATH")

app = FastAPI(title="Analytics API", version="1.0",
              docs_url=f'{CONTEXT_PATH}/documentation',
              redoc_url = None,
              openapi_url = f'{CONTEXT_PATH}/openapi.json'
)

# app.include_router(order_route, prefix=f'{CONTEXT_PATH}/api/v1',tags=["portfolio"])
@app.get(f'{CONTEXT_PATH}/ping',tags=["Ping"])
def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    logging.info(f'Running FastAPI app on port {os.getenv("PORT",80)}')
    uvicorn.run(app,host="0.0.0.0",port=int(os.getenv("PORT",80)))