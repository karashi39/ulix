from enum import StrEnum
import sys

from app.repository import Repository as Repo
from app.graphdb import GraphSession
from app.models import Node, Link


class Option(StrEnum):
    DELETE_ALL = "delete-all"


def delete_all() -> None:
    with GraphSession() as session:
        Repo.delete_all(session)


def create_testdata() -> None:
    mermaid_id = 1
    nodes = {
        "A": Node(mermaid_id=mermaid_id, name="A", display_name="Node A"),
        "B": Node(mermaid_id=mermaid_id, name="B", display_name="Node B"),
    }
    links = [
        Link(from_=nodes["A"], to=nodes["B"]),
    ]
    with GraphSession() as session:
        Repo.create_nodes(session, list(nodes.values()))
        Repo.create_links(session, links)
    print("Nodes created!")


def main(option: str) -> None:
    if option == Option.DELETE_ALL:
        delete_all()
        return
    create_testdata()


if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    main(option)
