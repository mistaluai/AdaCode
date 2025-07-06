from langchain.prompts import PromptTemplate

TEMPLATE = """
You are a world‑class computer‑science educator and curriculum designer.
Given exactly two LeetCode topics
- Topic A: {topic_a}
- Topic B: {topic_b}
Determine all pedagogically meaningful relationships between them, drawing ONLY from our predefined ontology:
{RELATIONSHIPS}

Instructions:
1. Analyze how Topic A and Topic B fit together in a learner’s progression
2. Use ONLY the relation keys listed above.
3. There might one or more relations apply
4. If *no* relation applies, return exactly: NONE in the relation field.
"""

relation_prompt = PromptTemplate.from_template(TEMPLATE)