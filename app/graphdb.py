from app.config import NEO4J_URI, NEO4J_AUTH
from neo4j import GraphDatabase


class GraphSession:
    def __enter__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
        self.session = self.driver.session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.driver.close()
