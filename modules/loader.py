

import csv
import pandas as pd

def load_class_data(filename):
    # with open(filename, "r") as f:
    #     data = csv.reader(f, delimiter=',')
    data = pd.read_csv(filename)
    return data


def load_titles_per_year(df, source, label):
    get_release_year(df)
    
    groups = df.groupby(['release_year'])

    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    years = groups.groups.keys()

    scores = titles_per_year

    return [years, scores]


def get_score(s, x10):
    sd = 0
    try:
        # sd = int(float(s))
        if x10:
            sd = float(s)*10
        else:
            sd = float(s)
    except:
        pass
    return sd

def get_release_year(df):
    if "release_date" in df:
        try:
            df["release_year"] = df["release_date"].apply(
                lambda e: int(e.split("-")[0]))
        except:
            df["release_year"] = df["release_date"]
    elif "release_year" in df:
        df["release_year"] = df["release_date"]
    else:
        df["release_year"] = df["year"]

def load_score_per_year(df, source, label, top_limit_group, x10 = False):

    get_release_year(df)
    df["score"] = df["score"].apply(lambda e: get_score(e, x10))

    df = pd.DataFrame(df, columns=['release_year', 'score'])

    filter = df["score"] != 0
    df = df[filter]

    print(df)

    groups = df.groupby(['release_year'])

    print("keys: ", groups.groups.keys())
    print("mean: ", groups.mean())

    # quit()

    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    max_titles_per_year = max(titles_per_year)
    titles_per_year_scaled = [e/max_titles_per_year for e in titles_per_year]

    print(titles_per_year)
    # print(titles_per_year_scaled)

    # quit()

    if top_limit_group is None:
        score_per_year = groups.mean()
    else:
        score_per_year = groups["score"].nlargest(
            top_limit_group).groupby(['release_year']).mean()

    print("groups: ")
    print(groups)

    print(groups.groups.keys())
    print(score_per_year.values)

    print("mean: ")
    print(score_per_year)

    # score_per_year = score_per_year.drop(columns=["rank"])

    years = groups.groups.keys()
    if top_limit_group is None:
        scores = [e[0] for e in score_per_year.values]
    else:
        scores = [e for e in score_per_year.values]

    scaled_scores = []
    for i, _ in enumerate(scores):
        scaled_scores.append(scores[i]*titles_per_year_scaled[i])

    return [years, scores]

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

