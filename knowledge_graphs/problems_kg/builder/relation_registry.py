from typing import Dict, Tuple, List
from similarity_metrics import compute_problem_similarity


def similar_to(
    p1: Dict,
    p2: Dict,
    params: Dict,
    graph_sim
) -> List[Tuple[str, str, str, Dict]]:
    """
    Create a SIMILAR_TO relation if the similarity between p1 and p2
    is above the specified threshold.
    """
    weights = params.get("weights")
    threshold = params["threshold"]

    # Compute detailed similarity components
    similarity_scores = compute_problem_similarity(p1, p2, graph_sim, weights)
    overall_similarity = similarity_scores["overall"]

    # Check if similarity is strong enough
    if overall_similarity >= threshold:
        source = str(p1["id"])
        target = str(p2["id"])
        relation_properties = similarity_scores
        return [(source, "SIMILAR_TO", target, relation_properties)]

    return []


def easier_than(
    p1: Dict,
    p2: Dict,
    params: Dict,
    graph_sim=None
) -> List[Tuple[str, str, str, Dict]]:
    """
    Create an EASIER_THAN relation if p1 is significantly easier than p2.
    """
    difficulty_gap = params["gap"]

    # Check if p1 is easier than p2 by more than the threshold
    if p1["difficulty"] < p2["difficulty"] - difficulty_gap:
        source = str(p1["id"])
        target = str(p2["id"])
        relation_properties = {
            "diff_gap": p2["difficulty"] - p1["difficulty"]
        }
        return [(source, "EASIER_THAN", target, relation_properties)]

    return []


def more_approachable_than(
    p1: Dict,
    p2: Dict,
    params: Dict,
    graph_sim=None
) -> List[Tuple[str, str, str, Dict]]:
    """
    Create a MORE_APPROACHABLE_THAN relation if p1 is noticeably more approachable than p2.
    """
    approach_gap_threshold = params["gap"]

    # Check if p1 is more approachable than p2 by more than the threshold
    if p1["approachability"] > p2["approachability"] + approach_gap_threshold:
        source = str(p1["id"])
        target = str(p2["id"])
        relation_properties = {
            "approach_gap": p1["approachability"] - p2["approachability"]
        }
        return [(source, "MORE_APPROACHABLE_THAN", target, relation_properties)]

    return []