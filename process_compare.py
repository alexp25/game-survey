import matplotlib.pyplot as plt
import csv
import pandas as pd
from graph import plot_barchart_multi_core
import matplotlib
import numpy as np
from statistics import stdev


def load_class_data(filename):
    # with open(filename, "r") as f:
    #     data = csv.reader(f, delimiter=',')
    data = pd.read_csv(filename)
    return data


def load_titles_per_year(df, source, label):
    df["release_year"] = df["release_date"].apply(
        lambda e: int(e.split("-")[0]))
    groups = df.groupby(['release_year'])

    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    years = groups.groups.keys()

    scores = titles_per_year

    return [years, scores]


def load_score_per_year(df, source, label):

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

    return [years, scores]

# first file must be ALL


files = ["./data/metacritic/class_data.csv", "./data/metacritic_action/class_data.csv", "./data/metacritic_adventure/class_data.csv", "./data/metacritic_rpg/class_data.csv",
         "./data/metacritic_fps/class_data.csv", "./data/metacritic_racing/class_data.csv", "./data/metacritic_rts/class_data.csv", "./data/metacritic_simulation/class_data.csv", "./data/metacritic_third_person/class_data.csv"]
names = ["All", "Action", "Adventure", "RPG",
         "FPS", "Racing", "RTS", "Simulation", "3PS"]

top_limit = None

plot_scores = True
# plot_scores = False

n_group = 3

top_limit_group = None
top_limit_group = 100

# top 10 pe perioada (grup)

if plot_scores:
    filename = "./figs/scores_per_year_combined"
else:
    filename = "./figs/titles_per_year_combined"

if top_limit_group is not None:
    filename += "_top_" + str(top_limit_group) + "_group"

filename += ".png"

data = []
scores_vect = []
colors = []
years_all = []
years_vect = []

got_years = False

# color_scheme = ['#481567FF', '#2D708EFF',
#                 '#FDE725FF', '#55C667FF', 'red', 'blue']

print(len(files))
cmap = matplotlib.cm.get_cmap('viridis')
color_scheme = [cmap(i) for i in np.linspace(0, 1, len(files))]
print(color_scheme)

# quit()


for i in range(len(files)):
    d = load_class_data(files[i])
    d["score"] = d["user_score"]

    # user score!
    d["score"] = d["user_score"]
    filter = d["user_score"] != "tbd"
    d = d[filter]
    d = d.sort_values(by=['user_score'], ascending=False)

    def get_score(s):
        sd = 0
        try:
            sd = int(float(s)*10)
        except:
            print("exception")
            pass
        return sd

    d["user_score"] = d["user_score"].apply(lambda e: get_score(e))

    if top_limit is not None:
        d = d[:top_limit]

    if plot_scores:
        years, scores = load_score_per_year(d, "metacritic", names[i])
    else:
        years, scores = load_titles_per_year(d, "metacritic", names[i])

    if not got_years:
        got_years = True
        years_all = years
    data.append(d)
    scores_vect.append(scores)
    years_vect.append(years)

# assign all to correct years index
# some years might be missing from some datasets (interpolate required)
scores_vect_processed = []

for i in range(len(files)):
    scores_processed = []
    # for all years in combined dataset
    for y in years_all:
        found = False
        index = 0
        # check years in curent dataset
        for yv_index, yv in enumerate(years_vect[i]):
            if y == yv:
                found = True
                index = yv_index
                break
        if not found:
            scores_processed.append(0)
        else:
            # print(index)
            scores_processed.append(scores_vect[i][index])
    scores_vect_processed.append(scores_processed)

# group by 5


scores_vect_processed_grouped = []
years_grouped = []


# print(len(years_all))

# quit()
i_group = 0
group_count = 0
avg_score = 0
year_start = 0
year_end = 0

year_start = str(list(years_all)[0])


for j, y in enumerate(years_all):
    i_group += 1
    if i_group >= n_group or j == len(years_all):
        i_group = 0
        year_end = str(y)
        years_grouped.append(year_start + "-" + year_end)
        year_start = str(y)

for i in range(len(files)):
    print(files[i])
    i_group = 0
    group_count = 0
    avg_score = 0
    scores_processed_grouped = []
    group_scores = []
    for j, y in enumerate(years_all):
        # print(y)
        crt_score = scores_vect_processed[i][j]
        group_scores.append(crt_score)
        avg_score += crt_score
        i_group += 1

        if i_group >= n_group or j == len(years_all):
            group_count += 1

            group_scores = sorted(group_scores, reverse=True)

            if top_limit_group is not None:
                group_scores = group_scores[:top_limit_group]
                # print(len(group_scores))
                avg_score = sum(group_scores)/len(group_scores)
            else:
                avg_score /= i_group

            scores_processed_grouped.append(avg_score)
            print(group_count, i_group, avg_score)
            avg_score = 0
            i_group = 0
            group_scores = []

    scores_vect_processed_grouped.append(scores_processed_grouped)
    has_years = True

print(years_grouped)
print(scores_vect_processed_grouped)

# get avg and stdev for all
all_scores_disp = []
for g in scores_vect_processed_grouped:
    for e in g:
        all_scores_disp.append(e)

avg_score_disp = sum(all_scores_disp)/len(all_scores_disp)
stdev_score_disp = stdev(all_scores_disp)

print(avg_score_disp)
print(stdev_score_disp)


# quit()
# plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
#                          "", years_grouped, [50,90], True, None, 0, None)

if plot_scores:
    # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
    #                          "Scores", years_grouped, [60,80], True, None, 0, None)
    # fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Average score",
    #                          "Average game scores by year (metacritic)", years_grouped, [60, 90], True, None, 0, None)

    fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Average score",
                                      "Average game scores by year (metacritic)", years_grouped, [avg_score_disp-stdev_score_disp, avg_score_disp+stdev_score_disp], True, None, 0, None)

    fig.savefig(filename, dpi=300)

    # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
    #                          "Scores", years_grouped, None, True, None, 0, None)

    # [0,100]
else:
    fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Number of titles",
                                      "Number of titles by year (metacritic)", years_grouped, [avg_score_disp-stdev_score_disp, avg_score_disp+stdev_score_disp], True, None, 0, None)

    fig.savefig(filename, dpi=300)
# plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
#                          "Title", years_grouped, [0, 40], True, None, 0, None)
