from enum import StrEnum
import sys

from app.repository import Repository as Repo
from app.graphdb import GraphSession
from app.models import Node, Link


class Option(StrEnum):
    DELETE_ALL = "delete-all"
    SELECT = "select"


def create_testdata(session, mermaid_id: int) -> None:
    nodes = {
        "A": Node(mermaid_id=mermaid_id, name="A", display_name="Node A"),
        "B": Node(mermaid_id=mermaid_id, name="B", display_name="Node B"),
    }
    links = [
        Link(from_=nodes["A"], to=nodes["B"]),
    ]
    Repo.create_nodes(session, list(nodes.values()))
    Repo.create_links(session, links)


def select(session, mermaid_id: int) -> None:
    result = Repo.select(session, mermaid_id)
    print(result)


def delete(session) -> None:
    Repo.delete_all(session)


def main(option: str) -> None:
    mermaid_id = 1
    with GraphSession() as session:
        if option == Option.DELETE_ALL:
            delete(session)
        if option == Option.SELECT:
            select(session, mermaid_id)
        else:
            create_testdata(session, mermaid_id)


if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    main(option)
