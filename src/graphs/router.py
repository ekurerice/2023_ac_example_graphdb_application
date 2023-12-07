import logging

from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from .daos import CompanyKnowledgeGraphDAO
from .models import Create, Read

api_router = APIRouter()

endpoint = "localhost"


@api_router.post("/graph/vertices", response_model=Create.Vertex.Response)
async def create_vertex(input: Create.Vertex.Request):
    logging.info(input)

    dao = CompanyKnowledgeGraphDAO(reader_endpoint=endpoint, writer_endpoint=endpoint)
    _ = await run_in_threadpool(dao.create_vertex, input.label, input.id)
    del dao

    return JSONResponse(Create.Vertex.Response(id=input.id).dict(), status_code=201)


@api_router.post("/graph/edges", response_model=Create.Edge.Response)
async def create_edge(input: Create.Edge.Request):
    logging.info(input)
    dao = CompanyKnowledgeGraphDAO(reader_endpoint=endpoint, writer_endpoint=endpoint)
    _ = await run_in_threadpool(dao.create_edge, input.label, input.id, input.v1.id, input.v2.id)
    del dao

    return JSONResponse(Create.Edge.Response(id=input.id).dict(), status_code=201)


@api_router.get("/graphs", response_model=Read.Graph.Response)
async def read_graphs(input: Read.Graph.Request):
    dao = CompanyKnowledgeGraphDAO(reader_endpoint=endpoint, writer_endpoint=endpoint)
    res = await run_in_threadpool(dao.read_graphs, input.label, input.data.key(), input.data.value())
    del dao

    response = Read.Graph.Response.transform_from_neptune_query_result(res)
    return JSONResponse(response.dict(), status_code=200)
