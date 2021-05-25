import matplotlib.pyplot as plt
import csv
import pandas as pd
import json


def load_class_data(filename):
    # with open(filename, "r") as f:
    #     data = csv.reader(f, delimiter=',')
    data = pd.read_csv(filename)
    return data


def save_csv(data, filename):
    stringdata = ""

    for row in data:
        for c, col in enumerate(row):
            stringdata += str(col)
            if c < len(row)-1:
                stringdata += ","
        stringdata += "\n"

    with open(filename, "w") as f:
        f.write(stringdata)


def plot_titles_per_year(df, source, label):
    try:
        df["release_year"] = df["release_date"].apply(
            lambda e: int(e.split("-")[0]))
    except:
        df["release_year"] = df["release_date"]

    df = df[df["release_year"] != 0]

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

    fig = plt.gcf()
    fig.savefig("./figs/titles_per_year_"+label+".png", dpi=300)

    plt.show()

    return scores, years


def get_score(s):
    sd = 0
    try:
        # sd = int(float(s)*10)
        sd = float(s)
    except:
        pass
    return sd


def plot_score_per_year(df, source, label):

    df = pd.DataFrame(df, columns=['release_date', 'score'])

    try:
        df["release_year"] = df["release_date"].apply(
            lambda e: int(e.split("-")[0]))
    except:
        df["release_year"] = df["release_date"]
    
    df = df[df["release_year"] != 0]

    df = df.drop(columns=["release_date"])

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

    print(years)

    # scores = scaled_scores

    # plt.bar(score_per_year)
    # color='blue'
    plt.bar(years, scores)
    plt.xlabel("Year")
    plt.ylabel("Average rating")
    plt.title("Average rating by year (" + source + ")")

    delta = (max(scores) - min(scores))/10
    plt.ylim([min(scores) - delta, max(scores) + delta])

    # plt.ylim([0, 100])
    # plt.xticks(years, scores)

    plt.legend([label])

    fig = plt.gcf()
    fig.savefig("./figs/score_per_year_"+label+".png", dpi=300)

    plt.show()

    return scores, years


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)


top_limit = None
# top_limit = 1000

min_score = None
# min_score = 80
# min_score = 70
# min_score = 65

# d = load_class_data("./data/metacritic_rpg/class_data.csv")
# d = load_class_data("./data/metacritic_fps/class_data.csv")
# d = load_class_data("./data/metacritic_racing/class_data.csv")
# d = load_class_data("./data/metacritic_rts/class_data.csv")
# d = load_class_data("./data/metacritic/class_data.csv")

d = load_class_data("./data/playstore_apps/health_fitness.csv")
class_name = "health_fitness"

# d = load_class_data("./data/playstore_apps/travel_local.csv")
# class_name = "travel_local"


# class_name = "PC"

# user score!
d["score"] = d["user_score"]

filter = d["score"] != "tbd"
d = d[filter]

d["score"] = d["score"].apply(lambda e: get_score(e))

except_last_year = 2020

try:
    filter = d["release_date"].apply(
        lambda e: int(e.split("-")[0])) != except_last_year
    d = d[filter]
except:
    filter = d["release_date"].apply(
        lambda e: int(e) != except_last_year)
    d = d[filter]
    pass

d = d.sort_values(by=['score'], ascending=False)

if top_limit is not None:
    d = d[:top_limit]


if min_score is not None:
    filter = d["score"].apply(
        lambda e: e >= min_score)
    d = d[filter]

print(d)

title = "metacritic"
title = "Play Store"

if top_limit is not None:
    title += " top " + str(top_limit)
    class_name += "_top_" + str(top_limit)

if min_score is not None:
    class_name += "_" + str(min_score)

scores, years = plot_score_per_year(d, title, class_name)
titles, years = plot_titles_per_year(d, title, class_name)

save_csv([scores], "./figs/score_per_year_"+class_name+".png.1.csv")
save_csv([titles], "./figs/titles_per_year_"+class_name+".png.1.csv")
save_csv([years], "./figs/years_"+class_name+".png.1.csv")
