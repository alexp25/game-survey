import matplotlib.pyplot as plt
import csv
import pandas as pd
import json


def load_class_data(filename):
    # with open(filename, "r") as f:
    #     data = csv.reader(f, delimiter=',')
    data = pd.read_csv(filename)
    return data


def plot_titles_per_year(df, source, label):
    df["release_year"] = df["release_date"].apply(
        lambda e: int(e.split("-")[0]))
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


def plot_score_per_year(df, source, label):

    df = pd.DataFrame(df, columns=['release_date', 'score'])

    df["release_year"] = df["release_date"].apply(
        lambda e: int(e.split("-")[0]))

    df = df.drop(columns=["release_date"])

    def get_score(s):
        sd = 0
        try:
            sd = int(float(s)*10)
        except:
            pass
        return sd

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

    # plt.ylim([0, 100])
    # plt.xticks(years, scores)

    plt.legend([label])

    fig = plt.gcf()
    fig.savefig("./figs/score_per_year_"+label+".png", dpi=300)

    plt.show()


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)


top_limit = None
# top_limit = 100

for k, thread in enumerate(config["threads"]):
    print("thread: " + str(k) + "/" + str(len(config["threads"])))

    folder = thread["out_folder"]

    class_data = load_class_data(folder + "/class_data.csv")
    class_name = thread["name"]

    # user score!
    class_data["score"] = class_data["user_score"]
    filter = class_data["user_score"] != "tbd"
    class_data = class_data[filter]
    class_data = class_data.sort_values(by=['user_score'], ascending=False)

    if top_limit is not None:
        class_data = class_data[:top_limit]

    print(class_data)

    title = "metacritic"
    if top_limit is not None:
        title += " top " + str(top_limit)

    plot_score_per_year(class_data, title, class_name)
    plot_titles_per_year(class_data, title, class_name)
