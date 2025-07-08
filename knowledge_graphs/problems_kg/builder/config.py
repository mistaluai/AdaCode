Topics_NEO4J_URI = "neo4j://127.0.0.1:7687"
Topics_NEO4J_PWD = "12345678"
Problems_NEO4J_CLEAR = True #disable if using in production
Problems_NEO4J_URI = ...
Problems_NEO4J_PWD = ...
RELATION_RULES = [
    {
        "name": "SIMILAR_TO",
        "function": "similar_to",
        "enabled": True,
        "params": {
            "threshold": 0.6,
            "weights": {
                "topics": 0.4,
                "difficulty": 0.2,
                "acceptance": 0.2,
                "graph": 0.2
            }
        }
    },
    {
        "name": "EASIER_THAN",
        "function": "easier_than",
        "enabled": True,
        "params": {
            "gap": 0.8
        }
    },
    {
        "name": "MORE_APPROACHABLE_THAN",
        "function": "more_approachable_than",
        "enabled": True,
        "params": {
            "gap": 0.3
        }
    }
]