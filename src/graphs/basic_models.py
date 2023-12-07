from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator

from .id_generator import IDGenerator


class Organization(BaseModel):
    organization_name: Optional[str]

    def hash(self):
        return IDGenerator.generate_vertex_id(self.organization_name)

    def key(self):
        return "organization_name"

    def value(self):
        return self.organization_name


class Individual(BaseModel):
    name: str

    def hash(self):
        return IDGenerator.generate_vertex_id(self.name)

    def key(self):
        return "name"

    def value(self):
        return self.name


class BasicVertex(BaseModel):
    """リクエストの頂点情報を持つモデル。"""

    @root_validator(pre=True)
    def set_data(cls, values):
        if values["label"] == "organization":
            data = Organization(
                organization_name=values.get("organization_name"),
            )
        elif values["label"] == "individual":
            data = Individual(
                name=values.get("name"),
            )

        values["data"] = data
        values["id"] = values["data"].hash()
        return values

    id: str
    label: Literal[
        "organization",
        "individual",
    ]

    # 共通プロパティ
    data: Union[Organization, Individual]


EdgeLabels = Literal["label"]
POSSIBLE_EDGE_LABELS = ["label"]


class BasicEdge(BaseModel):
    """リクエストのエッジの情報を持つモデル"""

    id: str
    label: EdgeLabels
    v1: BasicVertex
    v2: BasicVertex
    data: Optional[dict]

    @root_validator(pre=True)
    def set_values(cls, values):
        values["label"] = values.get("label") or "label"

        values["v1"] = BasicVertex(**values.get("v1"))
        values["v2"] = BasicVertex(**values.get("v2"))
        if not values.get("data"):
            values["data"] = {}

        values["id"] = IDGenerator.generate_edge_id(
            values["v1"].id,
            values["label"],
            values["v2"].id,
        )

        return values
