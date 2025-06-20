import sys
from enum import StrEnum

from app.repositories import *
from app.graphdb import exec_cypher


class Option(StrEnum):
    DELETE_ALL = "delete-all"


def main(option: str) -> None:
    if option == Option.DELETE_ALL:
        exec_cypher(delete_all)
        return

    mermaid_id = 1
    nodes = [
        {"node_name": "A", "display_name": "Node A"},
        {"node_name": "B", "display_name": "Node B"},
    ]
    for node in nodes:
        exec_cypher(create_node, node["display_name"], node["node_name"], mermaid_id)
    exec_cypher(create_link, "A", "B", mermaid_id)
    print("Nodes created!")


if __name__ == "__main__":
    option = sys.argv[1] if len(sys.argv) > 1 else ""
    main(option)
