from app.models import Node, Link
import re
from .syntax import Header, Arrow, Paren, COMMENT_LITERAL


def is_header(line: str) -> bool:
    return any(header.value in line for header in Header)


def contains_arrow(line: str) -> bool:
    return any(arrow.value in line for arrow in Arrow)


def get_arrow_label(arrow_part: str) -> str | None:
    if "|" not in arrow_part:
        return None
    pattern = r"\|(.*?)\|"
    match = re.search(pattern, arrow_part)
    if not match:
        return None
    return strip_quotes(match.group(1))


def strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return s[1:-1]
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1]
    return s


def reduce_space(line: str) -> str:
    pattern = r"\s+"
    return re.sub(pattern, " ", line.strip())


def get_node_params(node_text: str) -> tuple:
    text = node_text.strip()

    name = text
    dname = text
    ptype = None
    for paren in Paren:
        if paren.value[0] in text:
            name = text.split(paren.value[0])[0].replace('"', "").strip()
            dname = text.replace(name, "").replace('"', "").strip()[:-1][1:]
            ptype = paren.name
            break
    node_text.split("(")
    return name, dname, ptype


def loads(chart_id: int, lines: list[str]) -> list[Link]:
    links: list[tuple] = []
    name_to_dname = {}
    for line in lines:
        if not line:
            continue
        if is_header(line):
            continue
        if COMMENT_LITERAL in line:
            continue
        if contains_arrow(line):
            part = reduce_space(line).split(" ")
            f_name, f_dname, f_ptype = get_node_params(part[0])
            label = get_arrow_label(part[1])
            t_name, t_dname, t_ptype = get_node_params(part[2])
            links.append((f_name, t_name, label))
            if t_name != t_dname:
                name_to_dname[t_name] = t_dname
            if f_name != f_dname:
                name_to_dname[f_name] = f_dname
        else:
            name, dname, ptype = get_node_params(line)
            if name != dname:
                name_to_dname[name] = dname

    return [
        Link(
            from_=Node(
                chart_id=chart_id,
                name=link[0],
                display_name=name_to_dname.get(link[0], link[0]),
            ),
            to=Node(
                chart_id=chart_id,
                name=link[1],
                display_name=name_to_dname.get(link[1], link[1]),
            ),
            label=link[2],
        )
        for link in links
    ]
