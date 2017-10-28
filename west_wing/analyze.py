
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import process_data



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

if __name__ == '__main__':
    ax = plot_heatmap()
    plt.show()
    


