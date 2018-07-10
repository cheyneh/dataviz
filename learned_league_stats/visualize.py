
import os
import logging
logger = logging.getLogger()
logger.debug('loading visualize.py')

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from config import CONFIG

matplotlib.style.use('fivethirtyeight')

from process_data import Data

image_dir = CONFIG['image_dir']
# names_to_track = ['HombergerC', 'VatterV', 'PantoneJ', 'BrignallR']
# names_to_track = ['HombergerC', 'VatterV', 'EberhartR']
# names_to_track = ['PantoneJ', 'BrignallR']
names_to_track = CONFIG['names']
rundle = CONFIG['rundle']
data = Data(names_to_track)

# helper function to automatically plot all 'plotter' functions
plotters = []
def plotter(f):
    plotters.append(f)
    return f

def _plot_series(ctext=None):
    if ctext:
        with plt.style.context(ctext):
            fig, ax = plt.subplots()
    else:
        fig, ax = plt.subplots()
    df.plot(ax=ax)
    rank_max = df.max().max()

    return fig

@plotter
def plot_score_histogram():
    df = data.make_dataframe(key='score')
    fig, axs = plt.subplots(1, 2, sharey=True, figsize=(14, 8))

    df.plot.box(ax=axs[0], grid=False)
    df.plot.hist(ax=axs[1], bins=10, orientation='horizontal', 
            # align='right', 
            range=(-.5, 9.5),
            stacked=True)
    # for name in df.columns:
    #     sns.kdeplot(data=df[name], ax=axs[1], clip=(0,9))

    axs[0].set_title('Box Plot')
    axs[1].set_title('Stacked Histogram')
    axs[0].set_ylabel('Score')
    axs[1].set_xticks(range(0, 21, 5))
    axs[0].set_yticks(range(0, 10, 1))
    # axs[1].set_yticklabels([])
    fig.suptitle('Distribution of Daily Scores')

    return fig

@plotter
def plot_difficulty_heatmap():
    colors = [f'C{n}' for n in range(5)]
    ddf = data.get_average_difficulty()
    fig, axs = plt.subplots(1, len(names_to_track)+2,
            # sharey=True, 
            figsize=(12,12))

    # map difficulty [0-1] -> [.25, 1]
    ddf = 3*ddf/4 + .25

    # plot the first plot: average difficulty
    lcmap = lambda c: sns.light_palette(c, as_cmap=True)
    sns.heatmap(data=ddf, 
            ax=axs[0], 
            cbar=False, 
            vmin=0, vmax=1,
            cmap=lcmap('k'))

    # plot the last plot: average answers correct
    tdf = ddf.mean(axis=1) * 6
    tdf.plot.barh(ax=axs[-1], color='k', alpha=.7)
    axs[-1].set_yticks([])
    axs[-1].set_xticks(range(7))

    for idx, name in enumerate(names_to_track):
        ax = axs[idx+1]
        cdf  = data.get_correct(name) 
        cdf = cdf * ddf # correct times difficulty
        sns.heatmap(data=cdf, 
                ax=ax,
                cbar=False, 
                vmin=0, vmax=1,
                cmap=lcmap(f'C{idx}'))
        ax.set_title(name, fontsize=12)
        ax.set_xlabel('Question', fontsize=12)
        ax.set_yticks([])

    # axs[0].set_yticks(range(0, data.num_days, 2))
    yticklabels = [t.get_text() for t in axs[0].get_yticklabels()]

    axs[0].set_yticklabels(yticklabels, rotation=0)
    axs[0].set_ylabel('Match Day')
    axs[0].set_title('Avg Difficulty', fontsize=12)
    axs[0].set_xlabel('Question', fontsize=12)
    axs[-1].set_xlabel('Number Correct', fontsize=12)
    axs[-1].set_title('Avg Correct', fontsize=12)
    fig.suptitle(f'Correct Answers by Rundle {rundle} Difficulty')

    return fig

@plotter
def plot_total_correct():
    df = data.make_dataframe(key='tca', get_all=True)
    days, players = df.shape

    fig, ax = plt.subplots(figsize=(12,8))

    df.plot(ax=ax, legend=False, color='k', alpha=.2)
    df[names_to_track].plot(ax=ax, lw=5)
    ax.set_xlabel('Match Day')
    ax.set_ylabel('Correct Answers')
    l = ax.get_legend()
    l.draw_frame(True)
    ax.set_title('Cumulative Total Correct Answers')
    return fig

@plotter
def plot_all_ranks(callout_names=names_to_track):
    df = data.make_dataframe(key='rank', get_all=True)
    days, players = df.shape

    fig, ax = plt.subplots(figsize=(12,8))
    ax.invert_yaxis()

    df.plot(ax=ax, legend=False, color='k', alpha=.2)
    df[callout_names].plot(ax=ax, lw=5)
    ax.set_xlabel('Match Day')
    ax.set_ylabel('Rank')
    ax.set_xticks(range(1, 26, 2))
    ax.set_yticks(range(1, players+1, 5))
    l = ax.get_legend()
    l.draw_frame(True)
    ax.set_title(f'Relative Ranks in Rundle {rundle}')
    return fig

def plot_all():
    for f in plotters:
        name = f.__name__[5:]
        logger.info(f'plotting {name}')
        fig = f()
        fname = os.path.join(image_dir, f'{name}.png')
        fig.savefig(fname, dpi=240)
    plt.close('all')

if __name__ == '__main__':
    plot_all()


