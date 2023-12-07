from fastapi import FastAPI

from simplecheck.utils.logger import setup_logger

from graphs.router import api_router as graph_api_router
from visualized.router import api_router as visualized_api_router

app = FastAPI()
logger = setup_logger()


prefix = "/v1"

for i in [graph_api_router, visualized_api_router]:
    app.include_router(i, prefix=prefix)


@app.get("/status")
def status():
    return {"status": "ok"}
