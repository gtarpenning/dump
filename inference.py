import glob
import json
import numpy as np
import random
import os
from typing import List
import argparse
# import sklearn

NUM_EXAMPLES = 50
TARGET_KEY = {"energy":0, "productivity":1, "happiness":2}
TAG_ADJ_CORPUS = ["very", "low", "high"]
TAG_WORD_CORPUS = ["exercise", "work", "drinking", "food", "clean"]

"""
TODO:
    - take lists from the load_data() function and:
        - for target numpy array the target
        - for words one-hot-encode the words into a dict for tags and array the data (bound between 0,1)
    - put all the fake-data making in to a class with @classmethods
    - Make analysis with logistic regression 
    - Class the data loading and the ML inference.
"""


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

def make_fake_input(tag_len: List, adjective_thresh=0.5,):
    a,w = len(TAG_ADJ_CORPUS)-1, len(TAG_WORD_CORPUS)-1
    ret = []
    for k in tag_len:
        intermediate = []
        for i in range(k):
            if random.random() < adjective_thresh:
                intermediate.append(f"{TAG_ADJ_CORPUS[random.randint(0,a)]} {TAG_WORD_CORPUS[random.randint(0,w)]}")
            else:
                intermediate.append(f"{TAG_WORD_CORPUS[random.randint(0,w)]}")
        ret.append(intermediate)
    return ret

def make_fake_data(dir="data", num_vals=NUM_EXAMPLES, adjective_thresh=0.5, max_tags=5, username="user_1"):
    # we'll default write to user_1

    target = make_fake_target(num_vals)

    tag_len = [random.randint(1,max_tags) for i in range(num_vals)]
    X = make_fake_input(tag_len, adjective_thresh)

    fname = f"{username}_target.json"
    with open(os.path.join(dir, fname), 'w') as f:
        json.dump(target, f)

    fname = f"{username}_data.json"
    with open(os.path.join(dir, fname), 'w') as f:
        json.dump(X, f)

    return None

def load_data(dir="data", username="user_1"):
    user_files = glob.glob(os.path.join(dir, f"{username}*"))
    if len(user_files) != 2:
        raise Exception(f"User {username} should have exactly two files in {dir} not: {user_files}")
    
    target, data = None, None
    for fname in user_files:
        with open(fname, "r") as file:
            if "target" in fname:
                target = json.load(file)
            elif "data" in fname:
                data = json.load(file)
            else:
                raise Exception(f"File {fname} not of suffix 'data' or 'target'")
    
    if target is None or data is None:
        raise Exception(f"Loading from {user_files} failed.")
    
    return target, data

        

def get_tags():
    """Extract tags with a given prefix from the tags/ dir"""
    pass


def main(args):
    """testing"""

    # hardcoded at data
    if not glob.glob("./data/*.json") or args.force==True:
        make_fake_data() # use all defaults

    target, data = load_data(username=args.uname) # specifying user as an example
    print(f"{target=}\n\n {data=}")

    # # load test data
    # test_data = json.load(open("data/test_data.json", "r"))
    # make_insights(test_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data stuffs for lin reg")
    parser.add_argument("--uname", "-u", type=str, help="username", default="user_1")
    parser.add_argument("--force", "-f", action="store_true", default=False)
    args = parser.parse_args()

    main(args)
