from neo4j.graph import Node as Neo4jNode
from neo4j.graph import Relationship as Neo4jLink

from app.models import Node, Link


class Repository:
    @classmethod
    def create_node(cls, session, node: Node) -> Neo4jNode:
        query = """
        MERGE (n:Node {node_name: $node_name, mermaid_id: $mermaid_id})
        SET n.name = $display_name
        RETURN n
        """
        result = session.run(
            query,
            node_name=node.name,
            display_name=node.display_name,
            mermaid_id=node.mermaid_id,
        )
        return result.single()

    @classmethod
    def create_nodes(cls, session, nodes: list[Node]) -> list[Neo4jNode]:
        result = []
        for node in nodes:
            ret = cls.create_node(session, node)
            result.append(ret)
        return result

    @classmethod
    def create_link(cls, session, link: Link) -> Neo4jLink:
        query = (
            "MATCH (a:Node {node_name: $from_node, mermaid_id: $mermaid_id})"
            " MATCH (b:Node {node_name: $to_node, mermaid_id: $mermaid_id})"
            f" MERGE (a)-[r:{link.type_}]->(b)"
            " SET r.label = $label, r.link_type = $link_type"
            " RETURN r"
        )
        result = session.run(
            query,
            from_node=link.from_.name,
            to_node=link.to.name,
            mermaid_id=link.to.mermaid_id,
            link_type=link.type_,
            label=link.label,
        )
        return result.single()

    @classmethod
    def create_links(cls, session, links: list[Link]) -> list[Neo4jLink]:
        result = []
        for link in links:
            ret = cls.create_link(session, link)
            result.append(ret)
        return result

    @classmethod
    def delete_all(cls, session) -> None:
        query = "MATCH (n) DETACH DELETE n"
        session.run(query)
