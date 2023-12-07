import hashlib


class IDGenerator:
    @classmethod
    def generate_edge_id(cls, v1_id: str, label: str, v2_id: str):
        key = f"{v1_id}-{label}-{v2_id}"
        return hashlib.md5(key.encode()).hexdigest()

    @classmethod
    def generate_vertex_id(cls, key: str):
        return hashlib.md5(key.encode()).hexdigest()
