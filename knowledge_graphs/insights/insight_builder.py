"""
This module is responsible for parsing the raw text output from an LLM
and building a structured Student Insight Profile.

It is designed to work with free-text, by using regex
to find specially formatted headings (e.g., [HEADING_NAME]).
"""
import re
from typing import Dict, Any

# A mapping of the bracketed headings in the LLM's expected output to the
# keys in our final JSON profile.
INSIGHT_KEYS = {
    "COGNITIVE_GAP_ANALYSIS": "cognitive_gap",
    "PLAN-CODE_CONSISTENCY": "plan_code_consistency",
    "PATTERN_RECOGNITION_LEVEL": "pattern_recognition",
    "DEBUGGING_FORESIGHT": "debugging_foresight",
    "METACOGNITIVE_AWARENESS": "metacognitive_awareness",
}


def _extract_insight(llm_response: str, key: str) -> str:
    """
    Extracts the content for a single insight key from the LLM's response.

    Args:
        llm_response: The full text response from the LLM.
        key: The heading key to search for (e.g., "COGNITIVE_GAP_ANALYSIS").

    Returns:
        The extracted text, or a default message if the key is not found.
    """
    # This regex pattern finds content between a specific [KEY] and the next
    # bracketed heading or the end of the string.
    pattern = re.compile(
        r"\[" + re.escape(key) + r"\]\s*(.*?)(?=\s*\[[-A-Z_]+\]|\Z)",
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(llm_response)
    return match.group(1).strip() if match else "Insight not found."


def build_insight_profile(
    llm_response: str,
    problem_id: int,
    student_id: str,
    algorithmic_approach: str = "Not Analyzed",
    complexity_analysis: str = "Not Analyzed"
) -> Dict[str, Any]:
    """
    Parses the LLM's analysis and constructs a structured insight profile.
    """
    # Extract each insight from the LLM response using the predefined keys.
    insights = {
        json_key: _extract_insight(llm_response, heading_key)
        for heading_key, json_key in INSIGHT_KEYS.items()
    }

    # Assemble the final, structured profile.
    profile = {
        "problem_id": problem_id,
        "student_id": student_id,
        "insights": {
            "algorithmic_approach": algorithmic_approach,
            "complexity_analysis": complexity_analysis,
            **insights
        }
    }

    return profile
