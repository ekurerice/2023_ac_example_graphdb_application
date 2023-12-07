# from .utils import to_strT
import logging
import re
from typing import List

from gremlin_python.process.traversal import T
from pydantic import BaseModel, Field

from .basic_models import POSSIBLE_EDGE_LABELS, BasicEdge, BasicVertex, EdgeLabels


class Graph(BaseModel):
    class Vertex(BaseModel):
        id: str
        label: str
        properties: dict

    class Edge(BaseModel):
        id: str
        label: str
        link: List[int]
        properties: dict

    vertices: List[Vertex]
    edges: List[Edge]

    @classmethod
    def transform_from_neptune_query_result(cls, sequences):
        edges = []
        vertices = []

        vertex_id_to_position = {}
        edge_id_to_position = {}

        def check_property_key(key):
            if key in {T.label, T.id}:
                return False
            elif re.search("_id$", key):
                return False
            else:
                return True

        def record_to_edge(record, link: list):
            # Edgeケース
            property_keys = list(filter(check_property_key, record.keys()))
            properties = dict([(key, record[key]) for key in property_keys])

            edge = cls.Edge(id=record[T.id], label=record[T.label], link=link, properties=properties)
            return edge

        def record_to_vertex(record):
            # Nodeケース
            property_keys = list(filter(check_property_key, record.keys()))
            properties = dict([(key, record[key]) for key in property_keys])
            vertex = cls.Vertex(id=record[T.id], label=record[T.label], properties=properties)
            return vertex

        for records in sequences:
            batch_size = int((len(records) - 1) / 2)
            for batch in range(batch_size):
                position = batch * 2
                v1_record = records[position]
                e_record = records[position + 1]
                v2_record = records[position + 2]

                if v1_record[T.id] == v2_record[T.id]:
                    continue

                for v in [v1_record, v2_record]:
                    if v[T.id] not in vertex_id_to_position:
                        vertex = record_to_vertex(v)
                        vertices.append(vertex)
                        vertex_id_to_position[v[T.id]] = len(vertex_id_to_position)

                if e_record[T.id] not in edge_id_to_position:
                    link = [vertex_id_to_position[v1_record[T.id]], vertex_id_to_position[v2_record[T.id]]]
                    edge = record_to_edge(e_record, link)
                    edge_id_to_position[e_record[T.id]] = len(edge_id_to_position)
                    edges.append(edge)

        graph = Graph(vertices=vertices, edges=edges)
        return graph


class Create:
    class Vertex:
        class Request(BasicVertex):
            pass

        class Response(BaseModel):
            id: str

    class Edge:
        class Request(BasicEdge):
            pass

        class Response(BaseModel):
            id: str


class Read:
    class Graph:
        class Request(BasicVertex):
            edge_labels: List[EdgeLabels] = Field(POSSIBLE_EDGE_LABELS)

        class Response(Graph):
            pass
