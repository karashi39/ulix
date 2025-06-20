from app.config import NEO4J_URI, NEO4J_AUTH
from neo4j import GraphDatabase

def exec_cypher(tx_func, *args, mode="write", **kwargs):
    with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
        with driver.session() as session:
            if mode == "write":
                return session.write_transaction(tx_func, *args, **kwargs)
            else:
                return session.read_transaction(tx_func, *args, **kwargs)
