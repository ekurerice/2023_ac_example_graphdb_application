import json
from pathlib import Path

import pytest
from src.graphs.basic_models import BasicEdge, BasicVertex


class TestBasicModel:
    data_of_vertex = [
        (True, {"label": "individual", "name": "田中太郎"}),
        (True, {"label": "individual", "name": "山田一郎"}),
    ]

    @pytest.mark.parametrize("expected, item", data_of_vertex)
    def test_vertex(self, mocker, expected, item):
        actual = BasicVertex(**item)

    data_of_edge = [
        (True, {"label": "individual", "name": "山田一郎"}, {"label": "individual", "name": "田中太郎"}),
    ]

    @pytest.mark.parametrize("expected, v1, v2", data_of_edge)
    def test_edge(self, mocker, expected, v1, v2):
        BasicEdge(v1=v1, v2=v2)
