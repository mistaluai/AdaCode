import os
from pathlib import Path

from dotenv import load_dotenv

from kg_builder import get_topic_pairs, init_llm, generate_triples, build_graph

def main():
    # Load env
    load_dotenv(dotenv_path='/Users/mistaluai/Documents/Github Repos/AdaCode/.env')

    topic_pairs = get_topic_pairs()
    llm = init_llm()
    triples = generate_triples(llm, topic_pairs)

    graph = build_graph(triples)
    graph.serialize("../kg.ttl", format="turtle")
    print("Knowledge graph saved to kg.ttl")

if __name__ == "__main__":
    main()