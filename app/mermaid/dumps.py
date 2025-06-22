from app.models import Node, Link
from .syntax import Header, Arrow


def format_node(node: Node) -> str:
    if node.name != node.display_name:
        return f'{node.name}("{node.display_name}")'
    return node.name


def dumps(links: list[Link]) -> str:
    if not links:
        return ""

    chart_text = []
    chart_text.append(Header.LR.value)
    nodes = set()
    for link in links:
        nodes.add(link.from_)
        nodes.add(link.to)
        arrow = Arrow[link.type_]
        link_line = f"{link.from_.name} {arrow} {link.to.name}"
        chart_text.append(link_line)

    for node in nodes:
        node_line = format_node(node)
        chart_text.append(node_line)

    return "\n".join(chart_text)
