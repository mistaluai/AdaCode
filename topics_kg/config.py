import os
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(dotenv_path=os.path.join(Path.cwd().parent, '.env'))

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
    "Arrays",
    "Two Pointers"
]

TOPICS = [topic.replace(" ", "_").lower() for topic in RAW_TOPICS]