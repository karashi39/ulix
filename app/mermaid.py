from app.models import Node, Link
from enum import StrEnum


class Arrow(StrEnum):
    LINK = " --> "
    DOT = " -.-> "
    BOLD = " ==> "


def format_node(node: Node) -> str:
    if node.name != node.display_name:
        return f"{node.name}({node.display_name})"
    return node.name


class Mermaid:
    @classmethod
    def dump(cls, links: list[Link]) -> None:
        if not links:
            return
        print("flowchart LR")
        nodes = set()
        for link in links:
            nodes.add(link.from_)
            nodes.add(link.to)
            arrow = Arrow[link.type_]
            link_line = f"{link.from_.name} {arrow} {link.to.name}"
            print(link_line)

        for node in nodes:
            node_line = format_node(node)
            print(node_line)
