
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import FuncFormatter

import seaborn as sns

import process_data

NUM_SEASONS = 7

class Data(object):
    def __init__(self):
        self.raw_df = process_data.get_all_data()
        
    def trim(self, count=20):
        return self.raw_df.iloc[:, :count]

    def normalized_df(self, trim=None, relative=False):
        """Returns data frame normalized by the total number of lines in that
        scene. If relative is True, the normalization is by the number of
        lines by *those* characters."""

        if trim:
            df = self.trim(trim).T
        else:
            df = self.raw_df.copy().T

        if relative:
            totals = df.sum(axis=0)
        else:
            totals = self.raw_df.T.sum(axis=0)
        df = df / totals
        df = df.T.fillna(0)
        return df

    def rolling(self, trim=None, window=5, relative=False):
        df = self.normalized_df(trim, relative=relative)
        # bartlet windows because why not?
        rdf = df.rolling(window, win_type='bartlett', center=True).mean()
        return rdf

def plot_character_arcs(data, window=12, trim=10):
    df = data.rolling(trim=trim, window=window)
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111)
    df.plot(ax=ax, legend=False)
    seasons = list(df.index.get_level_values(0))
    season_starts = [seasons.index(s+1) for s in range(NUM_SEASONS)]
    index_anchors = [(season_starts[i]+season_starts[i+1])/2 
            for i in range(len(season_starts)-1)]
    index_anchors.append((season_starts[-1]+len(seasons))/2)

    ax.set_xticks(index_anchors)
    ax.set_xticklabels(range(1, NUM_SEASONS+1))

    for ix in range(len(season_starts[:-1])):
        if ix%2 == 0:
            continue
        x1 = season_starts[ix]
        x2 = season_starts[ix+1]
        ax.add_patch(
                patches.Rectangle(
                    (x1,0), 
                    x2-x1, 1,
                    facecolor='#000000',
                    alpha=0.1
                    )
                )
    ax.set_xlabel("Season")
    ax.set_ylabel("Percentage of Lines")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    ax.set_title("(Window size = {}".format(window))
    fig.suptitle("West Wing Character Prominence by Season")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, bbox_to_anchor=(1.2, .7))
    fig.subplots_adjust(right=.8)
    # fig.savefig(os.path.join('images', 'character_ts.png'), dpi=300)
    return fig

def plot_heatmap():
    df = process_data.get_data()

def plot_heatmap():
    df = process_data.character_df()

    # find top names
    name_counts = df.sum(axis=1).sort_values(ascending=False)
    top_names = name_counts.iloc[:20].index

    df = df.loc[top_names].fillna(0)

    counts = df.sum(axis=0)
    df = df / counts

    # weird outliers
    indices = list(df.columns)
    keep_indices = [idx for idx in indices if idx not in [145, 80, 67]]
    df = df.loc[:, keep_indices]


    ax = sns.heatmap(df, cmap='viridis')
    names = [t.get_text() for t in ax.get_yticklabels()]
    ax.set_yticklabels(names, rotation=0)
    return ax

def main():
    data = Data()

    char_arcs_10 = plot_character_arcs(data, window=10)
    fname = os.path.join('images', 'character_arcs_win10.png') 
    char_arcs_10.savefig(fname, dpi=300)

    char_arcs_20 = plot_character_arcs(data, window=20)
    fname = os.path.join('images', 'character_arcs_win20.png') 
    char_arcs_20.savefig(fname, dpi=300)

    plt.close('all')

if __name__ == '__main__':
    # data = Data()
    pass
    # ax = plot_heatmap()
    # plt.show()
    


