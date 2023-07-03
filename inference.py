import glob
import json
import numpy as np
import random
import os
from typing import List, Iterable, Dict
import argparse
from collections import OrderedDict
from sklearn.linear_model import LinearRegression

NUM_EXAMPLES = 50
TARGET_KEY = {"energy":0, "productivity":1, "happiness":2} #linspaced 0-n
TAG_ADJ_CORPUS = ["very", "low", "high"]
TAG_WORD_CORPUS = ["exercise", "work", "drinking", "food", "clean"]

"""
TODO:
    - Gen a ton of user data in files
    - Write a function to run through the user data
    - Create output API format for async function that does all the "ml" work

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
    
    @staticmethod
    def _unpack_coef_dict(d, t="\t\t"):
        """Returns a enter + $t seperated string of dict items k : v for coef unpacking"""
        return "".join([f"{t}{k} : {v*100:.2f}%\n" for k,v in d.items()])


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
    
    def numpify_target(self, target, squash=True):
        """
        target: List of Dicts

        Returns: np.array() with columns corresponding to TARGET_KEY and rows as samples
        """
        target = np.array([[t[k] for k in TARGET_KEY] for t in target])
        if squash:
            target = target/10 # We've enforced bounding between 1-10 #TODO catch with max?
        return target

    def numpify_data(self, data):
        """
        returns an array of shape: N, C
            C is the number of tags in the corpus

        TODO: one-hot encoding is gross we should use tokens like they are in text models -- just a list of token ids
        """
        ret = np.zeros((len(data), len(self.corpus),))
        for i, tags in enumerate(data):
            for t in tags:
                if self.ttoi(t) != -1:
                    ret[i][self.ttoi(t)] = 1
        return ret

class Learn:
    """
    Class to handle all the logic for learning? idk
    """

    def __init__(self, data_loader=None) -> None:
        self.fitted = False
        self.k = 3
        self.data_loader = data_loader

    def fit_models(self, data=None, target=None, use_loader=True):
        """
        assuming data, target are of json/raw format not numpified.
        """
        if self.fitted:
            print("Learn already fitted -- we do not support overwritting at the moment.")
            return
        if use_loader:
            if self.data_loader is None and (data is None or target is None):
                raise Exception("As self.data_loader is None you must provide data and target if using use_loader")
            elif self.data_loader is None:
                print("self.data_loader is None -- instantiating now")
                self.data_loader=DataLoader()
                self.data_loader.create_corpus(data)
                # TODO: handle filepaths? Refactor this whole dataloader bullshit to a DATAloader and a fileloader
            else:
                print("Using self.data_loader")
            X, y = self.data_loader.numpify_data(data), self.data_loader.numpify_target(target)

        else:
            print(f"{use_loader=} -- Assuming X = data and y = target")
            X, y = data, target

        self.models = {f"{k}_reg" : LinearRegression().fit(X, y[:,v]) for k,v in TARGET_KEY.items()}
        self.fitted=True



    def __str__(self):
        ret = ""
        if not self.fitted or self.data_loader is None:
            return self.__repr__()
        for k,v in self.models.items():
            sort_idx = np.argsort(v.coef_)
            worst, best = {self.data_loader.itot(i) : v.coef_[i] for i in sort_idx[:self.k]}, {self.data_loader.itot(i) : v.coef_[i] for i in sort_idx[-self.k:][::-1]}
            ret += f"Regression {k[:-3]}:\n\tBest {self.k}:\n{Preprocess._unpack_coef_dict(best)}\n\tWorst:\n{Preprocess._unpack_coef_dict(worst)}\n"
        return ret


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

    print("\n=========\n")
    print(f"{data_loader.numpify_target(target)=}")
    print(f"{data_loader.numpify_data(data)=}")

    print("\n=========\n")

    learner = Learn(data_loader)
    learner.fit_models(data, target, use_loader=True)
    print("\n=========\n")
    print(learner)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data stuffs for lin reg")
    parser.add_argument("--uname", "-u", type=str, help="username", default="user_1")
    parser.add_argument("--force", "-f", action="store_true", default=False)
    args = parser.parse_args()

    main(args)
