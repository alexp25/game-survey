import matplotlib.pyplot as plt
from modules import loader

def plot_titles_per_year(df, source, label, top_limit_group = None):
    [years, scores] = loader.load_titles_per_year(df, source, label)

    # plt.bar(score_per_year)
    # color='blue'
    plt.bar(years, scores)
    plt.xlabel("Year")
    plt.ylabel("Number of titles")
    plt.title("Number of titles by year (" + source + ")")

    delta = (max(scores) - min(scores))/10
    plt.ylim([min(scores) - delta, max(scores) + delta])
    # plt.ylim([50, 100])
    # plt.xticks(years, scores)

    plt.gca().grid(zorder=0)

    plt.legend([label])

    fig = plt.gcf()
    fig.savefig("./figs/titles_per_year_"+label+".png", dpi=300)

    plt.show()


def plot_score_per_year(df, source, label, x10 = None):

    [years, scores] = loader.load_score_per_year(df, source, label, None, x10)

    # print(years)
    # print(scores)
    # quit()
    # scores = scaled_scores

    # plt.bar(score_per_year)
    # color='blue'
    plt.bar(years, scores)
    plt.xlabel("Year")
    plt.ylabel("Average score")
    plt.title("Average game scores by year (" + source + ")")

    delta = (max(scores) - min(scores))/10
    plt.ylim([min(scores) - delta, max(scores) + delta])

    # plt.ylim([0, 100])
    # plt.xticks(years, scores)

    if x10:
        locs, labels = plt.yticks()  # Get the current locations and labels.
        yint = [int(e) for e in locs]
        ylabels = [e for e in labels]
        # plt.yticks(yint)
        ax = plt.gca()     
        ax.axes.yaxis.set_ticklabels(yint)

    plt.gca().grid(zorder=0)

    plt.legend([label])

    fig = plt.gcf()
    fig.savefig("./figs/score_per_year_"+label+".png", dpi=300)

    plt.show()