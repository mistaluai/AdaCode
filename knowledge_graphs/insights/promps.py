"""
Structured prompts to guide
both the student's submission and the LLM's analysis.
"""

def generate_student_facing_prompt(problem_name: str) -> str:
    """
    Generates the prompt that asks the student for a detailed, reflective solution.

    Args:
        problem_name: The name of the LeetCode problem.

    Returns:
        A formatted string to be presented to the student.
    """
    return f"""
For the problem "{problem_name}", please provide your solution in the following format.
Be thoughtful and detailed in each section.

[1. MY SOLUTION PLAN]
Before you write any code, describe your step-by-step plan to solve this problem. What data structures are you considering? What is your logic?

[2. MY CODE IMPLEMENTATION]
Write your Python code here.

[3. MY DATA STRUCTURE RATIONALE]
Explain *why* you chose the primary data structure(s) in your code. What are the trade-offs (e.g., time, space) of your choice compared to an alternative?

[4. MY EDGE CASES]
List the specific edge cases you considered and tested for (e.g., empty input, array with one element, no possible solution).

[5. MY CONFIDENCE & ALTERNATIVES]
How confident are you in this solution? Did you consider any alternative approaches before settling on this one? Briefly describe one.
"""


def generate_llm_analysis_prompt(problem_name: str, problem_description: str, student_submission: str) -> str:
    """
    Generates the prompt that asks the LLM to analyze the student's submission.

    Args:
        problem_name: The name of the LeetCode problem.
        problem_description: The full description of the problem.
        student_submission: The student's complete, structured response.

    Returns:
        A formatted string to be sent to the LLM for analysis.
    """
    return f"""
[SYSTEM]
You are an expert programming coach specializing in identifying cognitive patterns in student solutions. Analyze the following student submission for the LeetCode problem "{problem_name}".

[Problem Description]:
\"\"\"
{problem_description}
\"\"\"

[Student's Full Submission]:
\"\"\"
{student_submission}
\"\"\"

Based on the student's submission, provide a deep analysis. Use the exact headings provided below and provide a concise, expert analysis for each.

[COGNITIVE_GAP_ANALYSIS]
What is the single biggest gap in the student's thinking? Focus on the *reasoning*, not just the code. Examples: "Fails to connect problem requirements to data structure trade-offs," "Shows a pattern of missing off-by-one errors," "Relies on brute-force without considering optimization," "Misunderstands the core requirement of the problem."

[PLAN-CODE_CONSISTENCY]
Does the student's code faithfully implement their stated plan? Is the plan itself logical? Note any inconsistencies.

[PATTERN_RECOGNITION_LEVEL]
Does the student appear to recognize the underlying algorithmic pattern (e.g., "Two Pointers," "Sliding Window"), or are they just applying a memorized solution without understanding the 'why'?

[DEBUGGING_FORESIGHT]
Based on their "EDGE_CASES" section, how proactive and systematic is the student about testing and debugging? Do they foresee common pitfalls?

[METACOGNITIVE_AWARENESS]
Based on their "CONFIDENCE & ALTERNATIVES" section, how aware is the student of their own knowledge limits and the broader solution space?
"""
