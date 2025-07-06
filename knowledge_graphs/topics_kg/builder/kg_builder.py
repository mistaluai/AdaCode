import time
from itertools import permutations
from typing import List, Tuple

from tqdm import tqdm
from langchain.chat_models import init_chat_model

from config import TOPICS, MODEL_NAME, RELATIONSHIPS
from knowledge_graphs.topics_kg.builder.prompt import relation_prompt
from knowledge_graphs.topics_kg.builder.relation_schema import TopicRelation


def get_topic_pairs() -> List[Tuple[str, str]]:
    """Generate all ordered pairs of topics (excluding self-pairs)."""
    return list(permutations(TOPICS, 2))

def init_llm():
    """Initialize the chat model with TopicRelation structured output."""
    return init_chat_model(MODEL_NAME).with_structured_output(TopicRelation)

def generate_triples(llm, topic_pairs: List[Tuple[str, str]], delay: float = 1.5) -> List[Tuple[str, str, str, dict[str, str]]]:
    """
    Use the LLM to infer relationships between topic pairs and return valid triples with descriptions.

    Returns:
        List of (source, relation_type, target, description) tuples.
    """
    relation_chain = relation_prompt | llm
    triples = []

    try:
        for topic_a, topic_b in tqdm(topic_pairs, desc="Generating triples"):
            response: TopicRelation = relation_chain.invoke({
                "topic_a": topic_a,
                "topic_b": topic_b,
                "RELATIONSHIPS": RELATIONSHIPS
            })

            for rel in response.relations:
                if rel.type != "NONE":
                    triples.append((response.source, rel.type, response.target, {"description":rel.description}))

            time.sleep(delay)

    except Exception as e:
        print(f"[WARNING] Quota or invocation error: {e}")

    return triples