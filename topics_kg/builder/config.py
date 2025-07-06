import os
from pathlib import Path
from dotenv import load_dotenv

# Namespace base
NAMESPACE = "http://example.org/leetcode/"

# LLM model name
MODEL_NAME = "google_genai:gemini-2.5-flash"
# Relationships
RELATIONSHIPS = [
    ("IS_PREREQUISITE_OF", "A must be learned before B."),
    ("IS_SUBCONCEPT_OF", "A is a more specific or special case inside B."),
    ("USES_CONCEPT", "A depends on the use or understanding of B."),
    ("IS_STRATEGY_FOR", "A is a strategy used to approach B."),
    ("IS_DATA_STRUCTURE_FOR", "A is the structure typically used in B."),
    ("IS_REFORMULATION_OF", "A reframes B for easier reasoning or implementation."),
    ("IS_ANALOGOUS_TO", "A and B share similar structures or solving patterns."),
    ("IS_VARIATION_OF", "A is a minor or twisted version of B."),
    ("IS_OPTIMIZED_BY", "A becomes faster or better when B is applied."),
    ("IS_PARENT_TOPIC_OF", "A is a more general topic that B belongs to."),
    ("IS_SOLVED_BY", "B is a problem type typically addressed using A."),
    ("IS_SCAFFOLDED_BY", "A is used to develop the conceptual strength needed for B.")
]
ALLOWED_RELATION_TYPES = [r[0] for r in RELATIONSHIPS]

# Topics
RAW_TOPICS = [
    "Array",
    "String",
    "Hash Table",
    "Dynamic Programming",
    "Math",
    "Sorting",
    "Greedy",
    "Depth-First Search",
    "Binary Search",
    "Database",
    "Matrix",
    "Tree",
    "Bit Manipulation",
    "Breadth-First Search",
    "Two Pointers",
    "Prefix Sum",
    "Heap (Priority Queue)",
    "Simulation",
    "Binary Tree",
    "Stack",
    "Graph",
    "Counting",
    "Sliding Window",
    "Design",
    "Enumeration",
    "Backtracking",
    "Union Find",
    "Linked List",
    "Number Theory",
    "Ordered Set",
    "Monotonic Stack",
    "Segment Tree",
    "Trie",
    "Combinatorics",
    "Bitmask",
    "Queue",
    "Recursion",
    "Divide and Conquer",
    "Binary Indexed Tree",
    "Memoization",
    "Geometry",
    "Hash Function",
    "Binary Search Tree",
    "String Matching",
    "Topological Sort",
    "Shortest Path",
    "Rolling Hash",
    "Game Theory",
    "Interactive",
    "Data Stream",
    "Monotonic Queue",
    "Brainteaser",
    "Doubly-Linked List",
    "Randomized",
    "Merge Sort",
    "Counting Sort",
    "Iterator",
    "Concurrency",
    "Probability and Statistics",
    "Quickselect",
    "Suffix Array",
    "Line Sweep",
    "Minimum Spanning Tree",
    "Bucket Sort",
    "Shell",
    "Reservoir Sampling",
    "Strongly Connected Component",
    "Eulerian Circuit",
    "Radix Sort",
    "Rejection Sampling",
    "Biconnected Component"
]

TOPICS = [topic.replace(" ", "_").lower() for topic in RAW_TOPICS][:5]