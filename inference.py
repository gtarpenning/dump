import json
import random
from typing import Dict, List

NUM_EXAMPLES = 50
TARGET_KEY = {"energy": 0, "productivity": 1, "happiness": 2}
TAG_ADJ_CORPUS = ["very", "low", "high"]
TAG_WORD_CORPUS = ["exercise", "work", "drinking", "food", "clean"]


def make_insights(data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Longterm, this is a cronjob run daily/weekly/monthly to generate high-value insights"""

    return {"category": ["10% increase in energy when you sit"]}


def make_fake_target(num_vals: int = NUM_EXAMPLES) -> List[List[int]]:
    ret = []
    for i in range(num_vals):
        ret.append([random.randint(1, 10) for i in range(len(TARGET_KEY))])
    return ret


def make_fake_input(num_vals: int = NUM_EXAMPLES) -> List[str]:
    corp = []
    for i in range(num_vals):
        if random.random() < 0.5:
            corp += [
                f"{random.choice(TAG_ADJ_CORPUS)} {random.choice(TAG_WORD_CORPUS)}"
            ]
        else:
            corp += [f"{random.choice(TAG_WORD_CORPUS)}"]
    return corp


def get_tags() -> None:
    """Extract tags with a given prefix from the tags/ dir"""
    pass


def main() -> None:
    """testing"""

    # load test data
    try:
        test_data = json.load(open("data/test_data.json", "r"))
    except FileNotFoundError:
        print("No test data found, generating...")
        test_data = {"input": make_fake_input(), "target": make_fake_target()}
        json.dump(test_data, open("data/test_data.json", "w"))

    make_insights(test_data)


if __name__ == "__main__":
    main()
