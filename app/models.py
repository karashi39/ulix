from pydantic import BaseModel, model_validator
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
