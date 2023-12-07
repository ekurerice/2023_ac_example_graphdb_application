from __future__ import annotations

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python.structure.graph import Graph


class VertexNotFoundException(Exception):
    pass


class EdgeNotFoundException(Exception):
    pass


class CompanyKnowledgeGraphDAO:
    def __init__(self, reader_endpoint: str, writer_endpoint: str):
        if reader_endpoint == "localhost":
            self.reader_connection = DriverRemoteConnection(
                f"ws://{reader_endpoint}:8182/gremlin",
                "g",
            )
            self.writer_connection = DriverRemoteConnection(
                f"ws://{writer_endpoint}:8182/gremlin",
                "g",
            )
        else:
            # Note: プロダクトで記す場合、ここに本番環境向けのNeptuneの設定を記述する
            pass

        self.graph = Graph()
        self.reader_g = self.graph.traversal().with_remote(self.reader_connection)
        self.writer_g = self.graph.traversal().with_remote(self.writer_connection)

    def read_graphs(self, label: str, key: str, value: str):
        """サブグラフ検索用の汎用クエリ"""

        query = self.reader_g.V().has_label(label).has(key, value)

        for _ in range(2):
            query = query.both_e().both_v().not_(__.has_label(label).has(key, value))

        records = query.path().by(__.value_map(True)).to_list()

        return records

    def has_vertex(self, id):
        return True if self.reader_g.V().has_id(id).to_list() else False

    def create_vertex(self, label, id, **kwargs):
        if self.has_vertex(id):
            return
        query = self.writer_g.add_v(label)

        query.property(T.id, id)
        for k, v in kwargs.items():
            query.property(k, v)
        return query.iterate()

    def has_edge(self, id):
        return True if self.reader_g.E().has_id(id).to_list() else False

    def read_edge(self, id):
        # デバッグ用の関数
        if not self.has_edge(id):
            raise EdgeNotFoundException(f"該当のエッジ={id}が見つかりません")

        # Note: to_listが無いと、propertyの情報が戻らなかった
        property = self.reader_g.E().has_id(id).value_map().to_list()[0]
        return property

    def create_edge(self, label, id, v1_id, v2_id, **kwargs):
        if self.has_edge(id):
            return
        if not (self.has_vertex(v1_id) and self.has_vertex(v2_id)):
            raise VertexNotFoundException("該当のノードが見つかりません")
        query = self.writer_g.V(v1_id).add_e(label).to(__.V(v2_id))
        query.property(T.id, id)
        for k, v in kwargs.items():
            query.property(k, v)
        return query.iterate()

    def read_vertices(self):
        """デバッグ用の関数"""
        records = self.reader_g.V().limit(1000).path().by(__.value_map(True)).to_list()
        return records

    def __del__(self):
        self.reader_connection.close()
        self.writer_connection.close()
