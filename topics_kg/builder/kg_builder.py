import time
from itertools import permutations
from typing import List, Tuple

import langchain_google_genai
from tqdm import tqdm
from rdflib import Graph, Namespace
from langchain.chat_models import init_chat_model

from config import TOPICS, NAMESPACE, MODEL_NAME
from topics_kg.builder.config import RELATIONSHIPS
from topics_kg.builder.prompt import relation_prompt
from topics_kg.builder.relation_schema import TopicRelation


def get_topic_pairs() -> List[Tuple[str, str]]:
    """
    Generate all possible ordered pairs of topics (excluding self-pairs).

    Returns:
        List of (topic_a, topic_b) tuples.
    """
    return list(permutations(TOPICS, 2))


def init_llm():
    """
    Initialize the chat model with structured output schema (TopicRelation).

    Returns:
        LangChain chat model with TopicRelation structured output.
    """
    return init_chat_model(MODEL_NAME).with_structured_output(TopicRelation)


def generate_triples(llm, topic_pairs: List[Tuple[str, str]], delay: float = 1.5) -> List[Tuple[str, str, str]]:
    """
    Generate validated RDF triples using an LLM from topic pairs.

    Args:
        llm: A LangChain LLM chain with structured output.
        topic_pairs: List of topic pairs to evaluate relationships for.
        delay: Delay (in seconds) between LLM calls to avoid rate limits.

    Returns:
        List of validated (source, relation, target) triples.
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

            for relation in response.relations:
                triples.append((response.source, relation, response.target))

            time.sleep(delay)
    except Exception as e:
        print(f"Probably Quota Problem, saving whatever triples we got, error: {e}")

    return triples


def build_graph(triples: List[Tuple[str, str, str]]) -> Graph:
    """
    Build an RDF graph from a list of validated topic triples.

    Args:
        triples: List of (subject, predicate, object) tuples.

    Returns:
        An RDFLib Graph object with triples inserted.
    """
    g = Graph()
    EX = Namespace(NAMESPACE)
    g.bind("ex", EX)

    for subj, pred, obj in triples:
        subj_uri = EX[subj]
        pred_uri = EX[pred]
        obj_uri = EX[obj]
        g.add((subj_uri, pred_uri, obj_uri))

    return g