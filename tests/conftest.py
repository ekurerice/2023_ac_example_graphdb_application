from __future__ import annotations

import os
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from pytest import Config, Item, Parser

sys.path.append("src")

from src.graphs.basic_models import BasicEdge, BasicVertex  # noqa
from src.graphs.daos import CompanyKnowledgeGraphDAO  # noqa
from src.graphs.router import api_router as graph_api_router  # noqa

DEPENDENCIES: list = []


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    app = FastAPI()
    prefix = "/v1"
    for i in [graph_api_router]:
        app.include_router(i, prefix=prefix)

    host, port = "127.0.0.1", "9000"
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client


def pytest_addoption(parser: Parser) -> None:
    for dependency in DEPENDENCIES:
        parser.addoption(f"--{dependency}", action="store_true", default=False)


def pytest_configure(config: Config) -> None:
    for dependency in DEPENDENCIES:
        config.addinivalue_line("markers", dependency.replace("-", "_"))


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    for dependency in DEPENDENCIES:
        if config.getoption(f"--{dependency}"):
            continue
        skip = pytest.mark.skip(reason=f"need --{dependency} option to run")
        for item in items:
            if dependency.replace("-", "_") in item.keywords:
                item.add_marker(skip)


@pytest.fixture(scope="session")
def docker_compose_project_name():
    """
    pytest-docker が生成するコンテナのプレフィックスを指定する。
    デフォルトではランダムな文字列が生成されるが固定値を指定することで、
    pytest-docker が生成するコンテナのプレフィックスを固定するしています。
    """
    return "pytest_company_knowledge_graph_api"


@pytest.fixture(scope="session")
def docker_ip():
    return "localhost"


@pytest.fixture(scope="session")
def gremlin_service(docker_ip, docker_services):
    def is_responsive():
        try:
            dao = CompanyKnowledgeGraphDAO("localhost", "localhost")
            dao.read_vertices()
            return True
        except Exception:
            return False

    docker_services.wait_until_responsive(timeout=30.0, pause=1, check=is_responsive)

    # データ投入
    dao = CompanyKnowledgeGraphDAO(docker_ip, docker_ip)

    vertices = [
        {"label": "individual", "name": "A"},
        {"label": "individual", "name": "B"},
        {"label": "individual", "name": "C"},
        {"label": "individual", "name": "D"},
        {"label": "individual", "name": "E"},
        {"label": "individual", "name": "F"},
        {"label": "individual", "name": "G"},
        {"label": "individual", "name": "H"},
        {"label": "individual", "name": "I"},
        {"label": "individual", "name": "J"},
        {"label": "individual", "name": "K"},
    ]
    for vertex in vertices:
        basic_vertex = BasicVertex(**vertex)

        dao.create_vertex(
            basic_vertex.label, basic_vertex.id, **basic_vertex.data.dict()
        )

    edges = [
        {
            "label": "label",
            "v1": {"label": "individual", "name": "A"},
            "v2": {"label": "individual", "name": "C"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "B"},
            "v2": {"label": "individual", "name": "C"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "C"},
            "v2": {"label": "individual", "name": "D"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "C"},
            "v2": {"label": "individual", "name": "E"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "D"},
            "v2": {"label": "individual", "name": "F"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "D"},
            "v2": {"label": "individual", "name": "G"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "E"},
            "v2": {"label": "individual", "name": "G"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "F"},
            "v2": {"label": "individual", "name": "H"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "G"},
            "v2": {"label": "individual", "name": "H"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "H"},
            "v2": {"label": "individual", "name": "I"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "I"},
            "v2": {"label": "individual", "name": "J"},
        },
        {
            "label": "label",
            "v1": {"label": "individual", "name": "I"},
            "v2": {"label": "individual", "name": "K"},
        },
    ]

    for edge in edges:
        basic_edge = BasicEdge(**edge)
        dao.create_edge(
            basic_edge.label, basic_edge.id, basic_edge.v1.id, basic_edge.v2.id
        )

    return docker_ip
