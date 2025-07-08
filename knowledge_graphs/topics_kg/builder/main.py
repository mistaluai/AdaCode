from dotenv import load_dotenv

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
    load_dotenv("/Users/mistaluai/Documents/Github Repos/AdaCode/.env")
    print("Starting knowledge graph generation...")

    # Step 1: Generate topic pairs
    topic_pairs = get_topic_pairs()
    print(f"Prepared {len(topic_pairs)} topic pairs")

    # Step 2: Initialize the structured LLM
    llm = init_llm()
    print("LLM initialized with TopicRelation schema")

    # Step 3: Generate triples via LLM
    # triples = generate_triples(llm, topic_pairs)
    # Step 3: Use dummy triples for testing
    triples = [
        ("array", "RELATED_TO", "string", {"description": "Both are basic data types used in many problems."}),
        ("string", "IS_SIMILAR_TO", "array", {"description": "Both are basic data types used in many problems."}),

        ("binary_search", "IS_SIMILAR_TO", "divide_and_conquer",
         {"description": "Binary search is an example of divide and conquer."}),
        ("hash_table", "COVERS", "dictionary",
         {"description": "Hash tables are implemented using dictionaries in Python."}),
        ("linked_list", "MORE_PRIMITIVE_THAN", "tree",
         {"description": "Linked lists are simpler linear structures than trees."}),
    ]
    print(f"Generated {len(triples)} topic relationship triples")

    # Step 4: Push to Neo4j (topics graph)
    graph = Neo4jGraph(uri=NEO4J_URI, user="neo4j", password=NEO4J_PWD)
    graph.clear_topic_subgraph()
    # Extract all unique topic names from triples
    unique_topics = set()
    for source, _, target, _ in triples:
        unique_topics.add(source)
        unique_topics.add(target)

    # Create topic nodes
    graph.add_topic_nodes(list(unique_topics))

    # Create labeled relationships between them
    graph.add_relationships(triples, source_label="Topic", target_label="Topic")

    graph.close()
    print("Neo4j topic graph successfully built!")


if __name__ == "__main__":
    main()