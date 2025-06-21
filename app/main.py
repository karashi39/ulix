from enum import StrEnum
import sys

from app.repository import Repository as Repo
from app.graphdb import GraphSession
from app.models import Node, Link


class Option(StrEnum):
    DELETE_ALL = "delete-all"
    SELECT = "select"


def create_testdata(session, chart_id: int) -> None:
    nodes = {
        "A": Node(chart_id=chart_id, name="A", display_name="Node A"),
        "B": Node(chart_id=chart_id, name="B", display_name="Node B"),
    }
    links = [
        Link(from_=nodes["A"], to=nodes["B"]),
    ]
    Repo.create_nodes(session, list(nodes.values()))
    Repo.create_links(session, links)


def select(session, chart_id: int) -> None:
    result = Repo.select(session, chart_id)
    print(result)


def delete_all(session) -> None:
    Repo.delete_all(session)


def main(option: str) -> None:
    chart_id = 1
    with GraphSession() as session:
        if option == Option.DELETE_ALL:
            delete_all(session)
        elif option == Option.SELECT:
            select(session, chart_id)
        else:
            create_testdata(session, chart_id)


if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    main(option)
