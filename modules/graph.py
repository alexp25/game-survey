
import matplotlib.pyplot as plt
import csv
import math
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

FSIZE_TITLE = 20
FSIZE_LABEL = 18
FSIZE_LABEL_S = 18
FSIZE_LABEL_XS = 16
OPACITY = 0.9
rotation = 0

def set_rotation(rot):
    global rotation
    rotation = rot


def plot_barchart_multi_core(data, colors, labels, xlabel, ylabel, title, xlabels, limits, show, offset, bcount, legend_loc):
    global rotation

    fig, ax = plt.subplots(figsize=(10, 8))

    # ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=FSIZE_LABEL_XS)
    ax.tick_params(axis='both', which='minor', labelsize=FSIZE_LABEL_XS)

    n_groups = len(data)

    if bcount != 0:
        bar_width = 1 / (bcount + 1)
    else:
        bar_width = 1 / (n_groups + 1)

    if offset is None:
        # offset = -1 / (n_groups * 2 * bar_width + 1)
        if n_groups == 2:
            offset = bar_width / 2
        else:
            # offset = -bar_width / n_groups
            offset = -1 / ((n_groups + 1) / 2) - bar_width
            # offset = 0
            # offset = -1 / ((n_groups + 1) / 2) + bar_width*3/2
            # pass

    opacity = OPACITY

    low = None
    high = None

    for i in range(n_groups):

        print("plotting index: " + str(i))

        index = np.arange(len(data[i]))

        if len([d for d in data[i] if d != 0]) != 0:
            low1 = min([d for d in data[i] if d != 0])
        else:
            low1 = None
        
        high1 = max(data[i])

        if low is None:
            low = low1
            high = high1

        if low1 is not None:
            if low1 < low:
                low = low1
        if high1 is not None:
            if high1 > high:
                high = high1

        rb = plt.bar(
            index + offset + i * bar_width,
            data[i],
            bar_width,
            alpha=opacity,
            color=colors[i] if colors is not None else None,
            label=labels[i],
            zorder=3)

    plt.xlabel(xlabel, fontsize=FSIZE_LABEL)
    plt.ylabel(ylabel, fontsize=FSIZE_LABEL)
    plt.title(title, fontsize=FSIZE_TITLE)

    if n_groups == 1:
        plt.xticks(index, xlabels)
    else:
        plt.xticks(index + bar_width, xlabels)

    if not legend_loc:
        legend_loc = "upper left"

    plt.legend(loc=legend_loc, fontsize=FSIZE_LABEL_XS)

    plt.xticks(rotation=rotation)

    ax.grid(zorder=0) 

    print("low limit: ", low)
    print("high limit: ", high)
    # plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
    # plt.ylim([math.ceil(low-0.005*(high-low)), math.ceil(high+0.005*(high-low))])
    # plt.ylim([low, high])

    # kscale = 0.25
    kscale = 0.1   

    if limits is not None:
        low = limits[0]
        high = limits[1]
    else:
        high += kscale * high
        low -= kscale * low

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.ylim([low, high])

    # set_fontsize()
    plt.tight_layout()

    if show:
        print("show")
        plt.show()

    return fig, ax
