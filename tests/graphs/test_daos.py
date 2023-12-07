from __future__ import annotations

import pytest
from src.graphs.basic_models import POSSIBLE_EDGE_LABELS, BasicEdge, BasicVertex
from src.graphs.daos import CompanyKnowledgeGraphDAO, EdgeNotFoundException, VertexNotFoundException
from src.graphs.models import BasicVertex


class TestDAO:
    data_for_read_graphs = [
        (True, {"label": "individual", "name": "K"}),
        (False, {"label": "individual", "name": "unknown"}),
    ]

    @pytest.mark.parametrize("expected, item", data_for_read_graphs)
    def test_read_graphs(
        self,
        gremlin_service,
        expected,
        item,
    ):
        bv = BasicVertex(**item)
        dao = CompanyKnowledgeGraphDAO(gremlin_service, gremlin_service)
        result = dao.read_graphs(bv.label, bv.data.key(), bv.data.value())
        assert expected == bool(result)

    data_for_create_vertex = [
        (True, {"label": "individual", "name": "Z"}),
    ]

    @pytest.mark.parametrize("expected, item", data_for_create_vertex)
    def test_create_vertex(self, gremlin_service, expected, item):
        rv = BasicVertex(**item)
        dao = CompanyKnowledgeGraphDAO(gremlin_service, gremlin_service)
        dao.create_vertex(
            rv.label,
            rv.id,
        )

    data_for_create_edge = [
        (
            True,
            {
                "label": "label",
                "v1": {"label": "individual", "name": "A"},
                "v2": {"label": "individual", "name": "K"},
                "data": {"type": "additional"},
            },
        ),
        (
            False,
            {
                "label": "label",
                "v1": {"label": "individual", "name": "A"},
                "v2": {"label": "individual", "name": "unknown"},
                "data": {"type": "additional"},
            },
        ),
    ]

    @pytest.mark.parametrize("expected, edge", data_for_create_edge)
    def test_create_edge(self, gremlin_service, expected, edge):
        basic_edge = BasicEdge(**edge)

        if expected:
            dao = CompanyKnowledgeGraphDAO(gremlin_service, gremlin_service)
            dao.create_edge(basic_edge.label, basic_edge.id, basic_edge.v1.id, basic_edge.v2.id, **basic_edge.data)
        else:
            with pytest.raises(Exception):
                dao = CompanyKnowledgeGraphDAO(gremlin_service, gremlin_service)
                dao.create_edge(basic_edge.label, basic_edge.id, basic_edge.v1.id, basic_edge.v2.id, **basic_edge.data)
