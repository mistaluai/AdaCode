import pprint

import pandas as pd

DIFFICULTY_MAP = {"Easy": 0.0, "Medium": 1.0, "Hard": 2.0}
def parse_topics(raw):
    if pd.isna(raw):
        return set()
    return set(tag.strip().lower().replace(" ", "_").replace("-", "_") for tag in raw.split(","))

def load_problems(csv_path: str):
    # Skip the first 2 rows that contain metadata
    df = pd.read_csv(csv_path, skiprows=2)

    # Keep only the required rows and clean column names
    df.columns = [col.strip().replace('\n', ' ') for col in df.columns]
    df = df.dropna(subset=["Topics", "Difficulty", "Accept Rate"])
    # Filter for free problems
    df = df[df["Free?"] == "Yes"]

    # Clean and convert fields
    df["problem_id"] = df["ID"]
    df["problem_name"] = df["Problem Name"]
    df["topics"] = df["Topics"].apply(parse_topics)
    df["difficulty"] = df["Difficulty"].map(DIFFICULTY_MAP)
    df["acceptance"] = df["Accept Rate"].str.rstrip("%").astype(float) / 100

    # Build the structured list of dictionaries
    problems = []
    for _, row in df.iterrows():
        problems.append({
            "id": int(row["problem_id"]),
            "name": row["problem_name"],
            "topics": row["topics"],
            "difficulty": row["difficulty"],
            "acceptance": row["acceptance"]
        })

    return problems


if __name__ == "__main__":
    problems = load_problems("./leetcode_problems.csv")
    pprint.pprint(problems, indent=4)
