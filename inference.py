import glob
import json
import numpy as np
import random
import sklearn

NUM_EXAMPLES = 50
TARGET_KEY = {"energy":0, "productivity":1, "happiness":2}
TAG_ADJ_CORPUS = ["very", "low", "high"]
TAG_WORD_CORPUS = ["exercise", "work", "drinking", "food", "clean"]
TAG_CORPUS = [f"{TAG_ADJ_CORPUS[random.randint(0,len(TAG_ADJ_CORPUS))]} {TAG_WORD_CORPUS[random.randint(TAG_WORD_CORPUS)]}" for i in range(NUM_EXAMPLES) if rand.random(0,1) < 0.5 else f"{TAG_WORD_CORPUS[random.randint(0,len(TAG_WORD_CORPUS))]}"]


def make_insights(data: dict) -> dict:
    """ Longterm, this is a cronjob run daily/weekly/monthly to generate high-value insights """

    return {
        "category": "10% increase in energy when you sit"
    }


def make_fake_target(num_vals = NUM_EXAMPLES):
    ret = []
    for i in range(num_vals):
        ret.append([random.randint(1,10) for i in range(len(TARGET_KEY.keys()))])
    return ret

def make_fake_input(num_vals = 50):
    a,w = len(TAG_ADJ_CORPUS), len(TAG_WORD_CORPUS)
    ret = []
    for i in range(num_vals):
        if random.random(0,1) < 0.5:
            ret.append(f"{TAG_ADJ_CORPUS[random.randint(0,a)]} {TAG_WORD_CORPUS[random.randint(0,w)]}")
        else:
            ret.append(f"{TAG_WORD_CORPUS[random.randint(0,w)]}")
    return ret



def get_tags():
    """Extract tags with a given prefix from the tags/ dir"""
    pass


def main():
    """testing"""

    # load test data
    test_data = json.load(open("data/test_data.json", "r"))
    make_insights(test_data)


if __name__ == "__main__":
    main()
