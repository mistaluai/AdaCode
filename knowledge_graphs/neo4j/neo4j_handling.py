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

    def insert_relationship(self, tx, source: str, relation: str, target: str, properties: dict):
        """
        Insert a relationship with arbitrary properties.

        Args:
            tx: Neo4j transaction.
            source: Source topic name.
            relation: Relationship type.
            target: Target topic name.
            properties: Dictionary of properties to attach to the relationship.
        """
        # Build SET clauses dynamically from the properties dict
        set_clauses = ", ".join([f"r.{key} = ${key}" for key in properties.keys()])

        # Merge and set properties
        cypher = f"""
            MATCH (a:Topic {{name: $source}})
            MATCH (b:Topic {{name: $target}})
            MERGE (a)-[r:{relation}]->(b)
            SET {set_clauses}
        """

        tx.run(cypher, source=source, target=target, **properties)

    def add_knowledge_triples(self, triples: List[Tuple[str, str, str, dict[str, str]]]):
        """
        Insert nodes and edges with properties into Neo4j.

        Args:
            triples: A list of (source, relation_type, target, properties_dict) tuples.
        """
        with self.driver.session() as session:
            for source, relation, target, properties in triples:
                session.execute_write(self.insert_topic, source)
                session.execute_write(self.insert_topic, target)
                session.execute_write(self.insert_relationship, source, relation, target, properties)