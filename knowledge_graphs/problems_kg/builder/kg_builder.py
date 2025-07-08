from itertools import combinations
from config import RELATION_RULES
import relation_registry as registry
from tqdm import tqdm

def build_edges(problems, graph_sim=None):
    triples = []
    combs = list(combinations(problems, 2))
    for p1, p2 in tqdm(combs, desc='Building Relations'):
        for rule in RELATION_RULES:
            if not rule["enabled"]:
                continue

            fn_name = rule["function"]
            rule_fn = getattr(registry, fn_name)
            result = rule_fn(p1, p2, rule["params"], graph_sim)
            triples.extend(result)

    return triples
