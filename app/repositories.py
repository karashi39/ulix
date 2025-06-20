def create_node(tx, display_name, node_name, mermaid_id):
    query = """
    MERGE (n:Node {node_name: $node_name, mermaid_id: $mermaid_id})
    SET n.name = $display_name
    """
    result = tx.run(query, node_name=node_name, display_name=display_name, mermaid_id=mermaid_id)
    return result.single()

def delete_all(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)
