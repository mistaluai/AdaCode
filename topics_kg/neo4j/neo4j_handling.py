from typing import List, Tuple

from neo4j import GraphDatabase


class Neo4jGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="12345678", clear=False):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        if clear:
            self.clear_database()

    def close(self):
        self.driver.close()

    def clear_database(self):
        """Delete all nodes and relationships from the Neo4j database."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def insert_topic(self, tx, topic_name: str):
        """Ensure a topic node exists."""
        tx.run("""
            MERGE (:Topic {name: $name})
        """, name=topic_name)

    def insert_relationship(self, tx, source: str, relation: str, target: str, description: str):
        """Insert a relationship with type and description as a property."""
        tx.run(f"""
            MATCH (a:Topic {{name: $source}})
            MATCH (b:Topic {{name: $target}})
            MERGE (a)-[r:{relation}]->(b)
            SET r.description = $description
        """, source=source, target=target, description=description)

    def add_knowledge_triples(self, triples: List[Tuple[str, str, str, str]]):
        """
        Insert nodes and edges into Neo4j.

        Args:
            triples: A list of (source, relation_type, target, description) tuples.
        """
        with self.driver.session() as session:
            for source, relation, target, description in triples:
                session.execute_write(self.insert_topic, source)
                session.execute_write(self.insert_topic, target)
                session.execute_write(self.insert_relationship, source, relation, target, description)

