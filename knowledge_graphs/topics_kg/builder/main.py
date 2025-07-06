from knowledge_graphs.topics_kg.builder.config import NEO4J_URI, NEO4J_PWD, NEO4J_CLEAR
from knowledge_graphs.topics_kg.builder.kg_builder import (
    get_topic_pairs,
    init_llm,
    generate_triples,
)
from knowledge_graphs.neo4j.neo4j_handling import Neo4jGraph


def main():
    """
    Builds a conceptual knowledge graph from LeetCode topics by:
    - generating topic pairs,
    - querying LLM for their conceptual relations,
    - and storing the resulting triples in a Neo4j property graph.
    """
    print("Starting knowledge graph generation...")

    # 1. Get all pairwise topic combinations
    topic_pairs = get_topic_pairs()
    print(f"Prepared {len(topic_pairs)} topic pairs")

    # 2. Load LLM with structured TopicRelation output
    llm = init_llm()
    print("LLM initialized with schema")

    # 3. Generate knowledge triples using the LLM
    triples = generate_triples(llm, topic_pairs)
    print(f"Generated {len(triples)} relationship triples")

    # 4. Insert into Neo4j graph
    graph = Neo4jGraph(uri=NEO4J_URI, user="neo4j", password=NEO4J_PWD, clear=NEO4J_CLEAR)
    graph.add_knowledge_triples(triples)
    graph.close()
    print("Graph successfully built in Neo4j!")


if __name__ == "__main__":
    main()