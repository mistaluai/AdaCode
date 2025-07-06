import pprint
import pandas as pd
from math import exp

# Map difficulty levels to numerical values
DIFFICULTY_MAP = {"Easy": 0.0, "Medium": 1.0, "Hard": 2.0}


def sigmoid(x):
    return 1 / (1 + exp(-x))


def compute_approachability_with_normalization(
    difficulty: float,
    acceptance: float,
    min_acceptance: float,
    max_acceptance: float,
    alpha=5,
    beta=1.5
) -> float:
    """
    Dataset-aware approachability score that normalizes acceptance rate.

    Returns a value between 0 and 1.
    """
    if max_acceptance == min_acceptance:
        norm_acceptance = 0.5
    else:
        norm_acceptance = (acceptance - min_acceptance) / (max_acceptance - min_acceptance)

    score = alpha * norm_acceptance - beta * (difficulty ** 2)
    return sigmoid(score)


def parse_topics(raw):
    if pd.isna(raw):
        return set()
    return set(tag.strip().lower().replace(" ", "_").replace("-", "_") for tag in raw.split(","))


def load_problems(csv_path: str):
    # Skip the first 2 rows that contain metadata
    df = pd.read_csv(csv_path, skiprows=2)

    # Normalize column names
    df.columns = [col.strip().replace('\n', ' ') for col in df.columns]

    # Drop rows with missing critical fields
    df = df.dropna(subset=["Topics", "Difficulty", "Accept Rate"])

    # Filter only free problems
    df = df[df["Free?"] == "Yes"]

    # Clean and convert fields
    df["problem_id"] = df["ID"]
    df["problem_name"] = df["Problem Name"]
    df["topics"] = df["Topics"].apply(parse_topics)
    df["difficulty"] = df["Difficulty"].map(DIFFICULTY_MAP)
    df["acceptance"] = df["Accept Rate"].str.rstrip("%").astype(float) / 100

    # Compute min and max acceptance for normalization
    min_acceptance = df["acceptance"].min()
    max_acceptance = df["acceptance"].max()

    # Build structured list of dictionaries with approachability
    problems = []
    for _, row in df.iterrows():
        approachability = compute_approachability_with_normalization(
            row["difficulty"], row["acceptance"], min_acceptance, max_acceptance
        )

        problems.append({
            "id": int(row["problem_id"]),
            "name": row["problem_name"],
            "topics": row["topics"],
            "difficulty": row["difficulty"],
            "acceptance": row["acceptance"],
            "approachability": approachability
        })

    return problems


if __name__ == "__main__":
    problems = load_problems("./leetcode_problems.csv")
    pprint.pprint(problems, indent=4)