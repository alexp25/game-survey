import matplotlib.pyplot as plt
import csv
import pandas as pd
from modules.graph import plot_barchart_multi_core
import matplotlib
import numpy as np
from statistics import stdev
from modules import loader


folder = "./data/googlescholar/"

# files = [
#     folder + "result_database.blockchain.json.csv",
#     folder + "result_database.crowdsensing.json.csv",
#     folder + "result_database.serious_gaming.json.csv",
#     folder + "result_database.crowdsensing_blockchain.json.csv",
#     folder + "result_database_2.urban_water.json.csv",
#     folder + "result_database_2.blockchain_water.json.csv",
#     folder + "result_database_2.crowdsensing_water.json.csv"
# ]

# names = [
#     "Blockchain",
#     "Crowdsensing",
#     "Serious Gaming",
#     "Crowdsensing+Blockchain",
#     "Urban Water",
#     "Blockchain+Water",
#     "Crowdsensing+Water"
# ]

files = [
    folder + "result_database_processed.json.csv",
    folder + "result_database_merge.iot+water.json.csv",
    folder + "result_database_merge.big+data+water.json.csv",
    folder + "result_database_merge.anomaly+detection+water.json.csv",
    folder + "result_database_merge.decision+support+system+water.json.csv",
    folder + "result_database_merge.water+smart+cities+or+water+smart+city.json.csv",
]

names = [
    "All",
    "IoT + Water",
    "Big Data + Water",
    "Anomaly Detection + Water",
    "Decision Support System + Water",
    "Smart City + Water"
]


add_years = [[2006, 2007, 2010, 2011, 2012, 2013, 2014,
             2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]]
add_titles = [[1, 2, 1, 1, 1, 2, 4, 3, 10, 19, 25, 17, 22, 18, 5]]
add_names = ["References"]

add_years = []
add_titles = []
add_names = []

top_limit = None

# top_limit = 1000
# top_limit = 100

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

min_year = 2012

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
        d = loader.load_class_data(files[i])
        # index,keyword,title,details,year

        filter = d["year"] != "null"
        d = d[filter]

        if min_score is not None:
            filter = d["score"].apply(
                lambda e: e >= min_score)
            d = d[filter]

        if min_year is not None:
            filter = d["year"].apply(
                lambda e: e >= min_year)
            d = d[filter]

        d = d[filter]

        # d = d.sort_values(by=['score'], ascending=False)

        if top_limit is not None:
            d = d[:top_limit]

        print(len(d))

        # quit()

        if plot_scores:
            years, scores = loader.load_score_per_year(
                d, "metacritic", names[i], top_limit_group)
        else:
            years, scores = loader.load_titles_per_year(
                d, "metacritic", names[i])

        years = [int(y) for y in years]

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

    for add_years_vect in add_years:
        years_vect.append(add_years_vect)
    for add_titles_vect in add_titles:
        scores_vect_processed.append(add_titles_vect)
    for add_name in add_names:
        names.append(add_name)

    print(years_vect)
    print(scores_vect_processed)
    print(len(scores_vect_processed))
    print(len(scores_vect_processed[0]))

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
    loader.save_csv(scores_vect_processed_grouped, filename + ".csv")
    loader.save_csv([years_grouped], filename + ".years.csv")
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

        # -0.09
        fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Number of papers",
                                          "Number of papers by year (Google Scholar)", years_grouped, None, True, -0.2, 0, None)

        fig.savefig(filename, dpi=300)
    # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
    #                          "Title", years_grouped, [0, 40], True, None, 0, None)
