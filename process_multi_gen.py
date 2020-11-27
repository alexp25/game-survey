import matplotlib.pyplot as plt
import csv
import pandas as pd
import json
import math


def load_class_data(filename):
    # with open(filename, "r") as f:
    #     data = csv.reader(f, delimiter=',')
    data = pd.read_csv(filename)
    return data


def plot_titles_per_year(df, source, label):
    try:
        df["release_year"] = df["release_date"].apply(
            lambda e: int(e.split("-")[0]))
    except:
        df["release_year"] = df["release_date"]

    groups = df.groupby(['release_year'])

    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    years = groups.groups.keys()

    scores = titles_per_year

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

    plt.legend([label])

    plt.grid()

    fig = plt.gcf()
    fig.savefig("./figs/titles_per_year_"+label+".png", dpi=300)

    plt.show()


def downsample_list(rows, n, from_top):
    n_rows = len(rows)
    skip = int(n_rows / n) + 1
    new_list = []
    i = 0
    while True:
        index = i*skip
        if index < n_rows:
            new_list.append(rows[i*skip])
        else:
            break
        i = i + 1
    return new_list

def downsample_list_divn(rows, n):
    new_list = []
    for i in range(len(rows)):
        if i % n == 0:
            new_list.append(rows[i])
    return new_list

def get_score(s):
    sd = 0
    try:
        if x10:
            # sd = int(float(s)*10)
            sd = float(s) * 10
        else:
            sd = float(s)
    except:
        pass
    return sd

def plot_score_per_year(df, source, label, x10):

    df = pd.DataFrame(df, columns=['release_date', 'score'])

    try:
        df["release_year"] = df["release_date"].apply(
            lambda e: int(e.split("-")[0]))
    except:
        df["release_year"] = df["release_date"]

    df = df.drop(columns=["release_date"])

    df["score"] = df["score"].apply(lambda e: get_score(e))

    filter = df["score"] != 0
    df = df[filter]

    print(df)

    groups = df.groupby(['release_year'])

    print(groups.groups.keys())
    print(groups.mean())

    # quit()

    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    max_titles_per_year = max(titles_per_year)
    titles_per_year_scaled = [e/max_titles_per_year for e in titles_per_year]

    print(titles_per_year)
    # print(titles_per_year_scaled)

    # quit()

    score_per_year = groups.mean()

    print("groups: ")
    print(groups)

    print(groups.groups.keys(), score_per_year.values)

    print("mean: ")
    print(score_per_year)

    # score_per_year = score_per_year.drop(columns=["rank"])

    years = groups.groups.keys()
    scores = [e[0] for e in score_per_year.values]

    scaled_scores = []
    for i, _ in enumerate(scores):
        scaled_scores.append(scores[i]*titles_per_year_scaled[i])

    print(scaled_scores)

    # scores = scaled_scores

    # plt.bar(score_per_year)
    # color='blue'
    plt.bar(years, scores)
    plt.xlabel("Year")
    plt.ylabel("Average score")
    plt.title("Average game scores by year (" + source + ")")

    delta = (max(scores) - min(scores))/10
    plt.ylim([min(scores) - delta, max(scores) + delta])

    if x10:
        locs, labels = plt.yticks()  # Get the current locations and labels.
        yint = [int(e) for e in locs]
        ylabels = [e for e in labels]
        print(yint)
        print(ylabels)
        # plt.yticks(yint)
        ax = plt.gca()     
        ax.axes.yaxis.set_ticklabels(yint)

    plt.grid()
    plt.legend([label])

    fig = plt.gcf()
    fig.savefig("./figs/score_per_year_"+label+".png", dpi=300)

    plt.show()


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)


top_limit = None
# top_limit = 100

top_score = None
# top_score = 80
top_score = 4


class_data = load_class_data(
    "./data/playstore/archive_combined/result_database.android.3.playstore.json.csv")
class_name = "android"
title = "android"
x10 = False

# class_data = load_class_data("./data/metacritic_v2/result_database.json.csv")
# class_name = "ios"
# title = "iOS"
# x10 = False

# class_data = load_class_data(
#     "./data/metacritic_v2/result_database.console.json.csv")
# class_name = "console"
# title = "console"
# x10 = True

# class_data = load_class_data(
#     "./data/metacritic_v2/result_database.pc.json.csv")
# class_name = "PC"
# title = "PC"
# x10 = True


# user score!
class_data["score"] = class_data["user_score"]
filter = class_data["user_score"] != "tbd"
class_data = class_data[filter]
class_data = class_data.sort_values(by=['user_score'], ascending=False)

if top_limit is not None:
    class_data = class_data[:top_limit]

if top_score is not None:
    class_data["temp_score"] = class_data["score"].apply(lambda e: get_score(e))
    class_data = class_data[class_data['temp_score'] >= top_score]

# print(class_data)

if top_limit is not None:
    title += " top " + str(top_limit)
    class_name += " top " + str(top_limit)

if top_score is not None:
    title += " / score " + str(top_score) + "+"
    class_name += "_" + str(top_score)

plt.rc('axes', axisbelow=True)


plot_score_per_year(class_data, title, class_name, x10)
plot_titles_per_year(class_data, title, class_name)
