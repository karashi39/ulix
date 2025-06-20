def create_node(tx, display_name, node_name, mermaid_id):
    query = """
    MERGE (n:Node {node_name: $node_name, mermaid_id: $mermaid_id})
    SET n.name = $display_name
    """
    result = tx.run(query, node_name=node_name, display_name=display_name, mermaid_id=mermaid_id)
    return result.single()

def create_link(tx, from_node, to_node, mermaid_id, label=None):
    query = """
    MATCH (a:Node {node_name: $from_node, mermaid_id: $mermaid_id})
    MATCH (b:Node {node_name: $to_node, mermaid_id: $mermaid_id})
    MERGE (a)-[r:LINK]->(b)
    SET r.label = $label
    RETURN r
    """
    result = tx.run(
        query,
        from_node=from_node,
        to_node=to_node,
        mermaid_id=mermaid_id,
        label=label
    )
    return result.single()

def delete_all(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)
