import json

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from get_data import load_data

data = load_data()
# names = ['HombergerC', 'VatterV', 'PantoneJ', 'BrignallR']

class Data(object):
    """Represents the full set of data, with some helper functions to pull out
    bits and pieces of interest. The format is 
    [<day1_data>, <day2_data>, ..., <day25_data]
    where 
    <dayN_data> = [<user1_data>, <user2_data>, ..., <userK_data>]
    and
    <userN_data> = {key: value}, 
    with keys in the list
    ['username', 'ranks', 'points_{1,...,6}', 'result_{1,...,6}', 'points',
     'wins', 'tmp', 'ties', 'tca', '3pt', 'de', 'fl', 'losses', 'mpd']
    """

    def __init__(self, names):
        self.names = names
        self.raw_data = load_data()
        self.num_days = len(self.raw_data)
        self.num_players = len(self.raw_data[0])

    def make_dataframe(self, key='rank', get_all=False):
        """Makes a dataframe of the form day x row for the row and usernames
        given.""" 
        data = {}
        for day, day_data in enumerate(self.raw_data):
            day = day+1 # compensate for the 0-indexed list of days
            row_data = {}
            for user_data in day_data:
                uname = user_data['username']
                if not get_all and uname not in self.names:
                    continue

                # pull value from data
                if key == 'score':
                    value = Data._calculate_score(user_data, points=True)
                elif key == 'correct':
                    value = Data._calculate_score(user_data, points=False)
                else:
                    value = user_data[key]
                row_data[uname] = value
            data[day] = row_data
        return pd.DataFrame(data).T

    def get_average_difficulty(self):
        correct_data = {}
        for day, day_data in enumerate(self.raw_data):
            q_nums = [i+1 for i in range(6)]
            correct = {q: 0 for q in q_nums}
            for userdata in day_data:
                results = {q: userdata[f'result_{q}'] for q in q_nums}
                for key, val in results.items():
                    if val == 'Correct':
                        correct[key] += 1
            correct_data[day+1] = correct
        df = pd.DataFrame(correct_data, dtype=np.float).T 
        df = 1 - df/self.num_players
        return df

    def get_correct(self, name):
        correct_data = {}
        for day, day_data in enumerate(self.raw_data):
            q_nums = [i+1 for i in range(6)]
            for userdata in day_data:
                if userdata['username'] != name:
                    continue
                raw_res = {q: userdata[f'result_{q}'] for q in q_nums}
                res = {q: raw_res[q] == 'Correct' for q in raw_res}
            correct_data[day+1] = res
        df = pd.DataFrame(correct_data).T
        return df

    @staticmethod
    def _calculate_score(user_data, points=True):
        ans_nums = [i+1 for i in range(6)]
        # get the question results
        raw_results = [user_data[f'result_{num}'] for num in ans_nums]
        result_mapper = {'Wrong': 0, 'Forfeit': 0, 'Correct': 1}
        results = np.array([result_mapper[r] for r in raw_results])
        if not points:
            return results.sum()
        else:
            # get the question scores
            values = np.array([user_data[f'points_{num}'] for num in ans_nums])
            total_score = results.dot(values)
            return total_score


if __name__ == "__main__":
    data = Data()

    


