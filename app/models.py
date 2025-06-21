from pydantic import BaseModel, model_validator
from neo4j.graph import Node as Neo4jNode
from neo4j.graph import Relationship as Neo4jLink
from enum import StrEnum


class Node(BaseModel):
    mermaid_id: int
    name: str
    display_name: str | None = None

    @model_validator(mode="after")
    def set_default_display_name(self) -> "Node":
        if not self.display_name:  # None や 空文字も対象
            self.display_name = self.name
        return self

    @classmethod
    def from_neo4j(cls, neo_node: Neo4jNode):
        return cls(
            mermaid_id=neo_node["mermaid_id"],
            name=neo_node["node_name"],
            display_name=neo_node["name"],
        )


class LinkType(StrEnum):
    LINK = "LINK"
    DOT = "DOT"
    BOLD = "BOLD"


class Link(BaseModel):
    from_: Node
    to: Node
    type_: LinkType = LinkType.LINK
    label: str | None = None

    @model_validator(mode="after")
    def check_mermaid_id_match(self) -> "Link":
        if self.from_.mermaid_id == self.to.mermaid_id:
            return self
        raise ValueError("from_node and to_node must have the same mermaid_id")

    @classmethod
    def from_neo4j(cls, neo_link: Neo4jLink):
        if not neo_link.start_node or not neo_link.end_node:
            return None
        return cls(
            from_=Node.from_neo4j(neo_link.start_node),
            to=Node.from_neo4j(neo_link.end_node),
            type_=LinkType(neo_link.type),
            label=neo_link.get("label"),
        )
