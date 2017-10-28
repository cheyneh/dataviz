

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

import seaborn as sns
# sns.set_style('dark')

from mpmath import mp

N = 50000
mp.dps = N
PALETTE = 'magma'

CONSTANTS = {
        'pi'     : mp.pi,
        'e'      : mp.e,
        'phi'    : mp.phi,
        # 'euler'  : mp.euler,   # these are slow to calculate
        # 'mertens': mp.mertens,
        'sqrt2'  : mp.sqrt(2)
        }

def get_digits(constant):
    cstring = str(CONSTANTS[constant])
    cstring = cstring.replace('.', '')
    return cstring

def get_digit_to_step_translator(vector=np.array([1,0])):
    """Builds a fast lookup function for mapping digits to vectors."""
    increment = 2*np.pi / 10 
    steps = {}
    for idx, angle in enumerate(np.arange(0, 2*np.pi, increment)):
        rotation_matrix = np.array([
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]
                ])
        step = rotation_matrix.dot(vector)
        steps[str(idx)] = step
    def digit_to_step(digit):
        """Maps a (str) digit to a (vector) step."""
        return steps[digit]
    return digit_to_step

def get_segments(digits):
    digit_to_step = get_digit_to_step_translator()

    points = np.array([[0,0]] + [digit_to_step(d) for d in digits])
    points = points.cumsum(axis=0)

    points = points.reshape(-1, 1,  2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

def plot_walk(constant='pi', square=True, cmap=None, color=None, ax=None):
    segments = get_segments(get_digits(constant))
    max_x = segments[:,:,0].max()
    min_x = segments[:,:,0].min()
    max_y = segments[:,:,1].max()
    min_y = segments[:,:,1].min()
    if square:
        min_x = min_y = min([min_x, min_y])
        max_x = max_y = max([max_x, max_y])
    if cmap:
        lc = LineCollection(segments, cmap=cmap)
        lc.set_array(np.array(range(N)))
    elif color:
        lc = LineCollection(segments, color=color)
    else:
        lc = LineCollection(segments)

    if not ax:
        ax = plt.gca()
    ax.add_collection(lc)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    if square:
        ax.set_aspect('equal')
    return ax, lc, (min_x, max_x), (min_y, max_y)

def plot_all_grid():
    fig, axes = plt.subplots(2,2, figsize=(8,8))
    overall_lim = []
    for idx, constant in enumerate(CONSTANTS.keys()):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        ax, _, xlim, ylim = plot_walk(constant=constant, ax=ax,cmap=PALETTE)
        overall_lim.extend(xlim+ylim)
        ax.set_title(constant)
    overall_min = min(overall_lim)
    overall_max = max(overall_lim)
    for row in range(2):
        for col in range(2):
            axes[row, col].set_ylim(overall_min, overall_max)
            axes[row, col].set_xlim(overall_min, overall_max)
    return fig

def plot_all_single():
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    pal = sns.color_palette()
    overall_lim = []
    legend_handles = []
    legend_labels = []
    for color, constant in zip(pal, CONSTANTS.keys()):
        ax, handler, xlim, ylim = plot_walk(
                constant=constant, 
                ax=ax,
                color=color)
        overall_lim.extend(xlim+ylim)
        legend_handles.append(handler)
        legend_labels.append(constant)

    overall_min = min(overall_lim)
    overall_max = max(overall_lim)
    ax.set_xlim(overall_min, overall_max)
    ax.set_ylim(overall_min, overall_max)
    ax.legend(legend_handles, legend_labels, loc='lower right')
    ax.set_aspect('equal')
    fig.suptitle("Random Walks Generated by Decimal Representations")
    ax.set_ylabel("y")
    ax.set_xlabel("x")
    return fig

def plot_steps():
    steps = [str(i) for i in range(10)]
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    colors = sns.color_palette('husl', 10)
    legend_handles, legend_labels = [], []
    for c, s in zip(colors, steps):
        segments = get_segments(s)
        lc = LineCollection(segments, color=c)
        legend_handles.append(lc)
        legend_labels.append(s)
        ax.add_collection(lc)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(-1.5, 1.5)
    ax.legend(legend_handles, legend_labels)
    ax.set_aspect('equal')
    fig.suptitle('Steps Associated to Each Digit')
    return fig





def main():
    fig = plot_steps()
    fig.savefig('images/decimal_steps.png', dpi=150)
    fig.clf()


    fig = plot_all_single()
    fig.savefig('images/constant_single_plot.png', dpi=300)
    fig.clf()

    fig = plot_all_grid()
    fig.savefig('images/constant_grid_plot.png', dpi=300)
    fig.clf()

if __name__ == '__main__':
    main()









