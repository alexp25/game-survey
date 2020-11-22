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
    groups = df.groupby(['year'])

    titles_per_year = groups.count()
    titles_per_year = [e[0] for e in titles_per_year.values]

    years = groups.groups.keys()

    scores = titles_per_year

    return [years, scores]


def get_score(s):
    sd = 0
    try:
        # sd = int(float(s))
        sd = float(s)
    except:
        pass
    return sd


def load_score_per_year(df, source, label, top_limit_group):

    df = pd.DataFrame(df, columns=['year', 'index'])

    print(df)

    groups = df.groupby(['year'])

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

    if top_limit_group is None:
        score_per_year = groups.mean()
    else:
        score_per_year = groups["score"].nlargest(
            top_limit_group).groupby(['year']).mean()

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

# first file must be ALL


# files = ["./data/metacritic/class_data.csv", "./data/metacritic_action/class_data.csv", "./data/metacritic_adventure/class_data.csv", "./data/metacritic_rpg/class_data.csv",
#          "./data/metacritic_fps/class_data.csv", "./data/metacritic_racing/class_data.csv", "./data/metacritic_rts/class_data.csv", "./data/metacritic_simulation/class_data.csv", "./data/metacritic_third_person/class_data.csv"]
# names = ["All", "Action", "Adventure", "RPG",
#          "FPS", "Racing", "RTS", "Simulation", "3PS"]

folder = "./data/googlescholar/"

files = [
    folder + "result_database.blockchain.json.csv",
    folder + "result_database.crowdsensing.json.csv",
    folder + "result_database.serious_gaming.json.csv",
    folder + "result_database.crowdsensing_blockchain.json.csv"
]

names = [
    "Blockchain",
    "Crowdsensing",
    "Serious Gaming",
    "Crowdsensing+Blockchain"
]

top_limit = None

# top_limit = 1000
# top_limit = 100

plot_scores = True
plot_scores = False

min_score = None
# min_score = 80
# min_score = 70
# min_score = 65

# min_score = 3.5

# n_group = 5
n_group = 1

# top_limit_group_vect = [None, 1, 2, 3, 5, 10, 100]

top_limit_group_vect = [None]
# top_limit_group_vect = [1]

for top_limit_group in top_limit_group_vect:
    # top_limit_group = None
    # top_limit_group = 10

    # top 10 pe perioada (grup)

    if plot_scores:
        filename = "./figs/citations_per_year_googlescholar_combined"
    else:
        filename = "./figs/titles_per_year_googlescholar_combined"

    if top_limit_group is not None:
        filename += "_top_" + str(top_limit_group) + "_group"

    if top_limit is not None:
        filename += "_of_" + str(top_limit)

    if min_score is not None:
        filename += "_over_" + str(min_score)

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
        # index,keyword,title,details,year
       
        filter = d["year"] != "null"
        d = d[filter]

        if min_score is not None:
            filter = d["score"].apply(
                lambda e: e >= min_score)
            d = d[filter]

        d = d[filter]

        # d = d.sort_values(by=['score'], ascending=False)

        if top_limit is not None:
            d = d[:top_limit]

        print(len(d))

        # quit()

        if plot_scores:
            years, scores = load_score_per_year(
                d, "metacritic", names[i], top_limit_group)
        else:
            years, scores = load_titles_per_year(d, "metacritic", names[i])

        # print("scores: ", scores)

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
    print(scores_vect_processed)
    print(len(scores_vect_processed))
    print(len(scores_vect_processed[0]))
    # quit()

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
            if n_group == 1:
                years_grouped.append(year_end)
            else:
                years_grouped.append(year_start + "-" + year_end)
            year_start = str(y)

    for i in range(len(files)):
        print(files[i])
        i_group = 0
        i_group_avg = 0
        group_count = 0
        avg_score = 0
        scores_processed_grouped = []
        group_scores = []
        for j, y in enumerate(years_all):
            # print(y)
            crt_score = scores_vect_processed[i][j]
            # print(crt_score >= min_score)
            group_scores.append(crt_score)
            avg_score += crt_score
            i_group += 1
            if crt_score > 0:
                i_group_avg += 1

            if (i_group >= n_group) or (j == len(years_all)):
                group_count += 1

                group_scores = sorted(group_scores, reverse=True)
                print(group_scores)

                if top_limit_group is not None:
                    group_scores = group_scores[:top_limit_group]
                    # print(len(group_scores))
                    avg_score = sum(group_scores) / len(group_scores)
                else:
                    if i_group_avg > 0:
                        avg_score /= i_group_avg
                    else:
                        avg_score = 0

                scores_processed_grouped.append(avg_score)
                print(group_count, i_group_avg, avg_score)

                # quit()
                avg_score = 0
                i_group = 0
                i_group_avg = 0
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

    print(scores_vect_processed_grouped)
    save_csv(scores_vect_processed_grouped, filename + ".csv")
    save_csv([years_grouped], filename + ".years.csv")
    # quit()
    # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
    #                          "", years_grouped, [50,90], True, None, 0, None)

    if plot_scores:
        # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
        #                          "Scores", years_grouped, [60,80], True, None, 0, None)
        # fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Average score",
        #                          "Average game scores by year (metacritic)", years_grouped, [60, 90], True, None, 0, None)

        fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Average score",
                                          "Average paper scores by year (Google Scholar)", years_grouped, [avg_score_disp-stdev_score_disp*3, avg_score_disp+stdev_score_disp*3], True, None, 0, None)

        fig.savefig(filename, dpi=300)

        # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
        #                          "Scores", years_grouped, None, True, None, 0, None)

        # [0,100]
    else:
        # fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Number of titles",
        #                                   "Number of titles by year (metacritic)", years_grouped, [avg_score_disp-stdev_score_disp, avg_score_disp+stdev_score_disp], True, None, 0, None)

        fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Number of papers",
                                          "Number of papers by year (Google Scholar)", years_grouped, None, True, None, 0, None)

        fig.savefig(filename, dpi=300)
    # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
    #                          "Title", years_grouped, [0, 40], True, None, 0, None)
