from typing import List, Set, Dict
from math import exp
from neo4j import GraphDatabase

from knowledge_graphs.neo4j.neo4j_similarity import Neo4jGraphSim


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    Jaccard similarity between two sets.
    """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0.0


def difficulty_similarity(d1: float, d2: float) -> float:
    """
    Similarity between two difficulty scores using a sigmoid function.
    """
    gap = abs(d1 - d2)
    return 1 / (1 + exp(gap - 1))  # centered at gap = 1


def acceptance_similarity(a1: float, a2: float) -> float:
    """
    Similarity based on acceptance rate (1 - absolute difference).
    """
    return 1 - abs(a1 - a2)


def average_graph_similarity(topics1: Set[str], topics2: Set[str], graph_sim: Neo4jGraphSim) -> float:
    """
    Computes the average Neo4j graph-based similarity between all topic pairs.
    """
    if not topics1 or not topics2:
        return 0.0

    sims = [
        graph_sim.similarity(t1, t2)
        for t1 in topics1
        for t2 in topics2
        if t1 != t2
    ]

    return sum(sims) / len(sims) if sims else 0.0


def compute_problem_similarity(
    p1: Dict,
    p2: Dict,
    graph_sim: Neo4jGraphSim = None,
    weights: Dict[str, float] = None
) -> float:
    """
    Computes the similarity between two problems based on:
    - Topic overlap (Jaccard)
    - Difficulty proximity
    - Acceptance rate closeness
    - Graph-based conceptual similarity (optional)

    Each problem dict should contain:
        - "topics": Set[str]
        - "difficulty": float (e.g., Easy=0, Medium=1, Hard=2)
        - "acceptance": float between 0 and 1

    Args:
        p1, p2: Problem dictionaries
        graph_sim: Optional Neo4jGraphSim instance
        weights: Optional dict of similarity weights

    Returns:
        Final similarity score between 0 and 1.
    """
    weights = weights or {
        "topics": 0.5,
        "difficulty": 0.2,
        "acceptance": 0.2,
        "graph": 0.1
    }

    topic_sim = jaccard_similarity(p1["topics"], p2["topics"])
    diff_sim = difficulty_similarity(p1["difficulty"], p2["difficulty"])
    acc_sim = acceptance_similarity(p1["acceptance"], p2["acceptance"])
    graph_score = 0.0

    if graph_sim:
        graph_score = average_graph_similarity(p1["topics"], p2["topics"], graph_sim)

    final_score = {"overall": (
        weights["topics"] * topic_sim +
        weights["difficulty"] * diff_sim +
        weights["acceptance"] * acc_sim +
        weights["graph"] * graph_score
    ),
        "topic": topic_sim,
        "difficulty": diff_sim,
        "acceptance": acc_sim,
        "graph": graph_score
    }

    return final_score


if __name__ == "__main__":
    p1 = {
        "topics": {"array", "hash_table"},
        "difficulty": 0,  # Easy
        "acceptance": 0.56,
    }

    p2 = {
        "topics": {"hash_table", "string", "sliding_window", "array"},
        "difficulty": 0,  # Easy
        "acceptance": 0.37,
    }

    weights = {
        "topics": 0.4,
        "difficulty": 0.2,
        "acceptance": 0.1,
        "graph": 0.3
    }

    graph_sim = Neo4jGraphSim()
    score = compute_problem_similarity(p1, p2, graph_sim, weights)
    print(f"Similarity scores: {score}")
    graph_sim.close()