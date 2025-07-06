from neo4j import GraphDatabase


class Neo4jGraphSim:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="12345678"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def shortest_path_length(self, topic_a: str, topic_b: str) -> int:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Topic {name: $a}), (b:Topic {name: $b})
                MATCH p=shortestPath((a)-[*..10]-(b))
                RETURN length(p) AS path_length
            """, a=topic_a, b=topic_b)
            record = result.single()
            return record["path_length"] if record else 999  # No path

    def similarity(self, topic_a: str, topic_b: str) -> float:
        length = self.shortest_path_length(topic_a, topic_b)
        return 1 / (1 + length)  # Inverse