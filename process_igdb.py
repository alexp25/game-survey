import matplotlib.pyplot as plt
import csv
import pandas as pd
import json


def load_class_data(filename):
    # with open(filename, "r") as f:
    #     data = csv.reader(f, delimiter=',')
    data = pd.read_csv(filename)
    return data


def load_igdb(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
        data = json.loads(data)
    return data


def plot_titles_per_year(df, source, label):
    df = pd.DataFrame(df, columns=['release_date', 'score'])

    df["release_year"] = df["release_date"].apply(
        lambda e: int(e.split("-")[0]))

    df = df.drop(columns=["release_date"])

    groups = df.groupby(['release_year'])

    # score_per_year = groups.mean()
    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    years = groups.groups.keys()

    scores = titles_per_year

    plt.bar(years, scores)
    plt.xlabel("Year")
    plt.ylabel("Number of titles")
    plt.title("Number of titles by year (" + source + ")")

    delta = (max(scores) - min(scores))/10
    plt.ylim([min(scores) - delta, max(scores) + delta])
    # plt.xticks(years, scores)

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

    # score_per_year = groups.mean()
    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]
    max_titles_per_year = max(titles_per_year)
    titles_per_year_scaled = [e/max_titles_per_year for e in titles_per_year]

    print(titles_per_year)
    print(titles_per_year_scaled)

    # quit()
    score_per_year = groups.mean()

    print("groups: ")
    print(groups)
    print("mean: ")
    print(score_per_year)

    print(groups.groups.keys(), score_per_year.values)

    # score_per_year = score_per_year.drop(columns=["rank"])

    years = groups.groups.keys()
    scores = [e[0] for e in score_per_year.values]

    scaled_scores = []
    for i, _ in enumerate(scores):
        scaled_scores.append(scores[i]*titles_per_year_scaled[i])

    print(scaled_scores)

    # scores = scaled_scores
    # scores = titles_per_year

    # plt.bar(score_per_year)
    # color='blue'
    plt.bar(years, scores)
    plt.xlabel("Year")
    plt.ylabel("Average score")
    plt.title("Average game scores by year (" + source + ")")

    delta = (max(scores) - min(scores))/10
    plt.ylim([min(scores) - delta, max(scores) + delta])
    # plt.xticks(years, scores)

    fig = plt.gcf()
    fig.savefig("./figs/score_per_year_"+label+".png", dpi=300)

    plt.show()


def extract_igdb(data):
    csv_data = []
    params = []
    csv_data.append(
        ["rank,name,popularity,total_rating,total_rating_count,release_date,genre"])
    rank = 1
    for d in data:
        params.append(rank)
        params.append(d["name"].replace(",", ""))
        params.append(d["popularity"])
        params.append(d["total_rating"])
        params.append(d["total_rating_count"])
        params.append(d["release_dates"][0]["human"])
        if "genres" in d:
            params.append(d["genres"][0]["name"])
        else:
            params.append("NULL")
        csv_data.append(params)
        params = []
        rank += 1
    return csv_data


def load_igdb_df(filename):
    df = pd.read_csv(filename)
    df.sort_values(by=["total_rating"])
    df["score"] = df["total_rating"]
    df = df.drop(columns=["name", "popularity",
                          "total_rating", "total_rating_count", "genre"])
    return df


def stringify(csv_data):
    csv_string = ""
    rank = 1
    for d in csv_data:
        for i, c in enumerate(d):
            csv_string += str(c)
            if i < len(d) - 1:
                csv_string += ","
        csv_string += "\n"
        rank += 1
    return csv_string


plot = True
limit = 100
limit = None

class_data = load_class_data("./data/metacritic/class_data.csv")

if limit is not None:
    class_data = class_data[:limit]

# user score!
class_data["score"] = class_data["user_score"]

print(class_data)

json_data = load_igdb("./data/igdb/all.json")
class_data2 = extract_igdb(json_data)

class_data2 = stringify(class_data2)
# print(class_data2)

with open("./data/igdb/class_data.csv", "w") as f:
    f.write(class_data2)

df = load_igdb_df("./data/igdb/class_data.csv")

if limit is not None:
    df = df[:limit]

if plot:
    plot_score_per_year(df, "IGDB", "igdb")
    plot_titles_per_year(df, "IGDB", "igdb")


print(class_data)
print(df)
