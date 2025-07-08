from knowledge_graphs.neo4j.neo4j_handling import Neo4jGraph
from knowledge_graphs.neo4j.neo4j_similarity import Neo4jGraphSim
from knowledge_graphs.problems_kg.builder.kg_builder import build_edges
from knowledge_graphs.problems_kg.builder.problem_set_preprocessor import load_problems


def main():
    problems = load_problems("leetcode_problems.csv")[:200]
    print(f"Loaded {len(problems)} problems.")

    graph = Neo4jGraph(clear=False)
    graph.clear_problem_subgraph()

    graph.add_problem_nodes(problems)

    graph_sim = Neo4jGraphSim()
    triples = build_edges(problems, graph_sim)
    graph.add_problem_edges(triples)

    graph_sim.close()
    graph.close()
    print("Problem knowledge graph built successfully.")


if __name__ == "__main__":
    main()