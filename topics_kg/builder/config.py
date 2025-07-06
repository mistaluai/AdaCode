import os
from pathlib import Path
from dotenv import load_dotenv

# Namespace base
NAMESPACE = "http://example.org/leetcode/"

# LLM model name
MODEL_NAME = "google_genai:gemini-2.0-flash"
# Relationships
RELATIONSHIPS = [
    ("IS_PREREQUISITE_OF", "Topic A must be understood before Topic B; it is a foundational concept."),
    ("EXTENDS", "Topic B builds upon or generalizes Topic A, adding more complexity or scope."),
    ("OPTIMIZES", "Topic B is a more efficient or specialized version of Topic A for solving certain problems."),
    ("IS_IMPLEMENTED_WITH", "Topic B is commonly implemented using Topic A as a component or building block."),
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