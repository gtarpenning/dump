import glob
import json
import numpy as np
import random
import os
from typing import List, Iterable, Dict
import argparse
from collections import OrderedDict
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

LATE TODO:
    - there are a lot of things here that can be done by itertools or a apply method or something for code cleanliness
"""


class MakeFake:
    """
    Class for handling making fake things I recommend minimizing unless necessary
    Very useful for debuging and testing new functionality
    ----
    All methods should be @staticmethod or @classmethod
    """

    @classmethod
    def _target(cls, num_vals = NUM_EXAMPLES):
        ret = []
        for i in range(num_vals):
            ret.append({k : random.randint(1,10) for k in TARGET_KEY.keys()})
        return ret

    @classmethod
    def _input(cls, tag_len: List, adjective_thresh=0.5,):
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

    @classmethod
    def make_fake_data(cls,dir="data", num_vals=NUM_EXAMPLES, adjective_thresh=0.5, max_tags=5, username="user_1"):
        # we'll default write to user_1

        target = cls._target(num_vals)

        tag_len = [random.randint(1,max_tags) for i in range(num_vals)]
        X = cls._input(tag_len, adjective_thresh)

        fname = f"{username}_target.json"
        with open(os.path.join(dir, fname), 'w') as f:
            json.dump(target, f)

        fname = f"{username}_data.json"
        with open(os.path.join(dir, fname), 'w') as f:
            json.dump(X, f)

        return None


class Preprocess:
    """
    Class to handle preprocessing

    Input: string
    Output: string

    Use Preprocess.compose() with an iterable of Preprocess functors to run them in sequence
    """
    # TODO: replace with a composed method
    @staticmethod
    def lower_hyphen(t):
        return t.lower().replace(' ', '-')
    
    def lower(t):
        return t.lower()
    
    def space_replace(t, replace='-'):
        return t.replace(' ', replace)
    
    # TODO handle kwargs in iterables?
    @staticmethod
    def compose(functors: Iterable, s):
        for f in functors:
            s = f(s)
        return s


class DataLoader:
    """
    Class to handle all of the data loading
    """

    def __init__(self) -> None:
        self.corpus=None
        pass

    # def __len__(self):
    #     if self.corpus is None:
    #         raise Exception("You are checking the length without defining a corpus")
    #     return len(self.corpus)
    
    def create_corpus(self, tags: Iterable) -> OrderedDict:
        """
        Accepts an iterable List of Lists for tags 
        Returns a 1-hot-encoded dict of unique tags in an OrderedDict
            k : v = word : index
        """
        i = 0
        corpus = OrderedDict()
        if self.corpus is not None:
            print(f"You are UPDATING self.corpus with new tags. Please set self.corpus to None to overwrite current corpus.")
            i = self.corpus.values[-1]
            corpus = self.corpus
        for tag in tags:
            for t in tag:
                # preprocess:
                t = Preprocess.lower_hyphen(t)
                if corpus.get(t) is None:
                    corpus[t] = i
                    i+=1
        
        self.corpus = corpus

    # @classmethod # is this better for inheritance???
    def ttoi(self, tag): 
        return self.corpus[tag] if self.corpus.get(tag) is not None else -1
    def itot(self, index):
        return list(self.corpus.keys())[index] if index >= 0 and index <= len(self.corpus) else "" # errors when corpus is None but whatever -- maybe make it oogabooga on else for fun

    @staticmethod 
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
    
    def numpify_target(self, target):
        """
        target: List of Dicts

        Returns: np.array() with columns corresponding to TARGET_KEY and rows as samples
        """
        for ratings in target:
            
        


def make_insights(data: dict) -> Dict:
    """ Longterm, this is a cronjob run daily/weekly/monthly to generate high-value insights """

    return {
        "category": "10% increase in energy when you sit"
    }

        

def get_tags():
    """Extract tags with a given prefix from the tags/ dir"""
    pass


def main(args):
    """testing"""

    # hardcoded at data
    if not glob.glob("./data/*.json") or args.force==True:
        MakeFake.make_fake_data() # use all defaults

    target, data = DataLoader.load_data(username=args.uname) # specifying user as an example
    # print(f"{target=}\n\n {data=}")

    print("==========")

    data_loader = DataLoader()
    data_loader.create_corpus(data)

    print(f"{data_loader.corpus=}")

    print(f"TTOI 'exercise': {data_loader.ttoi('exercise')}")
    print(f"ITOT '14': {data_loader.itot(14)}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data stuffs for lin reg")
    parser.add_argument("--uname", "-u", type=str, help="username", default="user_1")
    parser.add_argument("--force", "-f", action="store_true", default=False)
    args = parser.parse_args()

    main(args)
