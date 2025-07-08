# knowledge_graphs/neo4j/neo4j_handling.py

from typing import List, Tuple, Dict
from neo4j import GraphDatabase
from tqdm import tqdm

class Neo4jGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="12345678", clear=False):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        if clear:
            self.clear_database()

    def close(self):
        self.driver.close()

    # -----------------------------
    # GRAPH CLEARING
    # -----------------------------

    def clear_database(self):
        """Clear all nodes and relationships (both problems and topics)."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def clear_problem_subgraph(self):
        """Delete only Problem nodes and their relationships."""
        with self.driver.session() as session:
            session.run("MATCH (p:Problem) DETACH DELETE p")

    def clear_topic_subgraph(self):
        """Delete only Topic nodes and their relationships."""
        with self.driver.session() as session:
            session.run("MATCH (t:Topic) DETACH DELETE t")

    # -----------------------------
    # INSERTING NODES
    # -----------------------------

    @staticmethod
    def insert_problem(tx, problem_id: str, problem_name: str):
        """Ensure a problem node exists with its ID and name."""
        tx.run("""
            MERGE (p:Problem {id: $id})
            SET p.name = $name
        """, id=problem_id, name=problem_name)

    @staticmethod
    def insert_topic(tx, topic_name: str):
        """Ensure a topic node exists."""
        tx.run("MERGE (t:Topic {name: $name})", name=topic_name)

    # -----------------------------
    # INSERTING RELATIONSHIPS
    # -----------------------------

    @staticmethod
    def insert_relationship(tx,
                            source_label: str, source_key: str,
                            relation: str,
                            target_label: str, target_key: str,
                            properties: Dict):
        """
        Create a relationship between two nodes using their labels and keys.

        Args:
            source_label: "Problem" or "Topic"
            source_key:   problem id or topic name
            relation:     relationship type string
            target_label: "Problem" or "Topic"
            target_key:   id or name depending on label
            properties:   dict of relationship properties
        """
        source_id_field = "id" if source_label == "Problem" else "name"
        target_id_field = "id" if target_label == "Problem" else "name"

        set_clause = ", ".join([f"r.{k} = ${k}" for k in properties]) if properties else ""

        cypher = f"""
            MATCH (a:{source_label} {{ {source_id_field}: $source_key }})
            MATCH (b:{target_label} {{ {target_id_field}: $target_key }})
            MERGE (a)-[r:{relation}]->(b)
            {"SET " + set_clause if set_clause else ""}
        """
        tx.run(cypher, source_key=source_key, target_key=target_key, **properties)

    # -----------------------------
    # BULK BUILDERS
    # -----------------------------

    def add_problem_nodes(self, problems: List[Dict]):
        """Insert a list of problems as nodes."""
        with self.driver.session() as session:
            for prob in problems:
                session.write_transaction(self.insert_problem, str(prob["id"]), prob["name"])

    def add_topic_nodes(self, topics: List[str]):
        """Insert a list of topic nodes."""
        with self.driver.session() as session:
            for topic in topics:
                session.write_transaction(self.insert_topic, topic)

    def add_relationships(self,
                          triples: List[Tuple[str, str, str, Dict]],
                          source_label: str,
                          target_label: str):
        """Generic batch insertion of relationships."""
        with self.driver.session() as session:
            for source, rel, target, props in tqdm(triples, desc="Inserting relationships"):
                session.write_transaction(
                    self.insert_relationship,
                    source_label, source,
                    rel,
                    target_label, target,
                    props
                )

    def add_problem_edges(self, triples: List[Tuple[str, str, str, Dict]]):
        """Shortcut: insert problem–problem relationships."""
        self.add_relationships(triples, source_label="Problem", target_label="Problem")

    def add_topic_edges(self, triples: List[Tuple[str, str, str, Dict]]):
        """Shortcut: insert topic–topic relationships."""
        self.add_relationships(triples, source_label="Topic", target_label="Topic")

    def add_problem_topic_edges(self, triples: List[Tuple[str, str, str, Dict]]):
        """Insert edges connecting Problem → Topic."""
        self.add_relationships(triples, source_label="Problem", target_label="Topic")