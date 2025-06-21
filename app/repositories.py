from app.models import Node, Link


def create_node(session, node: Node):
    query = """
    MERGE (n:Node {node_name: $node_name, mermaid_id: $mermaid_id})
    SET n.name = $display_name
    """
    result = session.run(
        query,
        node_name=node.name,
        display_name=node.display_name,
        mermaid_id=node.mermaid_id,
    )
    return result.single()


def create_link(session, link: Link):
    query = """
    MATCH (a:Node {node_name: $from_node, mermaid_id: $mermaid_id})
    MATCH (b:Node {node_name: $to_node, mermaid_id: $mermaid_id})
    MERGE (a)-[r:LINK]->(b)
    SET r.label = $label
    RETURN r
    """
    result = session.run(
        query,
        from_node=link.from_.name,
        to_node=link.to.name,
        mermaid_id=link.to.mermaid_id,
        label=link.label,
    )
    return result.single()


def delete_all(session):
    query = "MATCH (n) DETACH DELETE n"
    session.run(query)
