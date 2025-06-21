from app.models import Node, Link
import re
from enum import StrEnum, Enum

HEADER = "flowchart LR"


class Arrow(StrEnum):
    LINK = "-->"
    DOT = "-.->"
    BOLD = "==>"


class Paren(Enum):
    PAREN = ("(", ")")
    BRACKET = ("[", "]")


def contains_arrow(line: str) -> bool:
    return any(arrow.value in line for arrow in Arrow)


def format_node(node: Node) -> str:
    if node.name != node.display_name:
        return f"{node.name}({node.display_name})"
    return node.name


def reduce_space(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def get_node_params(node_text: str) -> tuple:
    text = node_text.strip()

    name = text
    dname = text
    ptype = None
    for paren in Paren:
        if paren.value[0] in text:
            name = text.split(paren.value[0])[0].strip()
            dname = text.split(paren.value[0])[1].replace(paren.value[1], "").strip()
            ptype = paren.name
            break
    node_text.split("(")
    return name, dname, ptype


class Mermaid:
    @classmethod
    def loads(cls, chart_id: int, lines: list[str]) -> list[Link]:
        links: list[tuple] = []
        name_to_dname = {}
        for line in lines:
            if not line:
                continue
            if HEADER in line:
                continue
            if contains_arrow(line):
                part = reduce_space(line).split(" ")
                f_name, f_dname, f_ptype = get_node_params(part[0])
                t_name, t_dname, t_ptype = get_node_params(part[2])
                links.append((f_name, t_name))
                name_to_dname[t_name] = t_dname
                name_to_dname[f_name] = f_dname
            else:
                name, dname, ptype = get_node_params(line)
                name_to_dname[name] = dname

        return [
            Link(
                from_=Node(
                    chart_id=chart_id, name=link[0], display_name=name_to_dname[link[0]]
                ),
                to=Node(
                    chart_id=chart_id, name=link[1], display_name=name_to_dname[link[1]]
                ),
            )
            for link in links
        ]

    @classmethod
    def dumps(cls, links: list[Link]) -> None:
        if not links:
            return
        print(HEADER)
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
