import sys
from enum import StrEnum

from app.repositories import delete_all, create_link, create_node
from app.graphdb import GraphSession
from app.models import Node, Link


class Option(StrEnum):
    DELETE_ALL = "delete-all"


def main(option: str) -> None:
    if option == Option.DELETE_ALL:
        with GraphSession() as session:
            delete_all(session)
        return

    mermaid_id = 1
    nodes = {
        "A": Node(mermaid_id=mermaid_id, name="A", display_name="Node A"),
        "B": Node(mermaid_id=mermaid_id, name="B", display_name="Node B"),
    }
    links = [
        Link(from_=nodes["A"], to=nodes["B"]),
    ]
    with GraphSession() as session:
        for node in nodes.values():
            create_node(session, node)
        for link in links:
            create_link(session, link)
    print("Nodes created!")


if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    main(option)
