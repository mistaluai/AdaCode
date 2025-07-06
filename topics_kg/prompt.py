from langchain.prompts import PromptTemplate

TEMPLATE = """
You are an expert in computer science education. Given the following two LeetCode topics:
- Topic A: {topic_a}
- Topic B: {topic_b}

Determine whether there is a meaningful conceptual relationship from A to B.
If so, respond with one of the following relation types ONLY:
{RELATIONSHIPS}

Otherwise, return NONE.

Respond with a valid RDF relation type only (no extra text), like:
IS_PREREQUISITE_OF

If no meaningful directed relation exists, return:
NONE
"""

relation_prompt = PromptTemplate.from_template(TEMPLATE)