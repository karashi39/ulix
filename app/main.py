from enum import StrEnum
import sys

from app.repository import Repository as Repo
from app.graphdb import GraphSession
from app.models import Node, Link
from app.mermaid import Mermaid


class Option(StrEnum):
    TEST_DATA = "test-data"
    DELETE_ALL = "delete-all"
    DUMP = "dump"


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


def dump(session, chart_id: int) -> None:
    links = Repo.select(session, chart_id)
    Mermaid.dumps(links)


def delete_all(session) -> None:
    Repo.delete_all(session)


def main(option: str) -> None:
    chart_id = 1
    with GraphSession() as session:
        if option == Option.DELETE_ALL:
            delete_all(session)
        elif option == Option.DUMP:
            dump(session, chart_id)
        elif option == Option.TEST_DATA:
            create_testdata(session, chart_id)
        else:
            input_data = sys.stdin.read()
            links = Mermaid.loads(chart_id, input_data.split("\n"))
            print(links)


if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    main(option)
