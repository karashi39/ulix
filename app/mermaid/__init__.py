from app.models import Link
from .loads import loads as loads_
from .dumps import dumps as dumps_


class Mermaid:
    @classmethod
    def loads(cls, chart_id: int, lines: list[str]) -> list[Link]:
        return loads_(chart_id, lines)

    @classmethod
    def dumps(cls, links: list[Link]) -> str:
        return dumps_(links)
