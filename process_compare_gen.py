import matplotlib.pyplot as plt
import csv
import pandas as pd
from modules.graph import plot_barchart_multi_core
import matplotlib
import numpy as np
from statistics import stdev
from modules import loader

# first file must be ALL


files = ["./data/metacritic/class_data.csv", "./data/metacritic_action/class_data.csv", "./data/metacritic_adventure/class_data.csv", "./data/metacritic_rpg/class_data.csv",
         "./data/metacritic_fps/class_data.csv", "./data/metacritic_racing/class_data.csv", "./data/metacritic_rts/class_data.csv", "./data/metacritic_simulation/class_data.csv", "./data/metacritic_third_person/class_data.csv"]
names = ["All", "Action", "Adventure", "RPG",
         "FPS", "Racing", "RTS", "Simulation", "3PS"]

platform = "pc"
title = "metacritic"
n_group = 5
x10 = True
stdev_factor = 1


# folder = "./data/metacritic_v2/"

# files = [
#     folder + "result_database.ps2.json.csv",
#     folder + "result_database.ps3.json.csv",
#     folder + "result_database.ps4.json.csv",
#     folder + "result_database.wii.json.csv",
#     folder + "result_database.xbox.json.csv",
#     folder + "result_database.xbox360.json.csv",
#     folder + "result_database.xboxone.json.csv",
#     folder + "result_database.ds.json.csv"
# ]

# names = [
#     "PS2",
#     "PS3",
#     "PS4",
#     "Wii",
#     "Xbox",
#     "Xbox360",
#     "Xbox One",
#     "DS"
# ]

# platform = "console_type"
# title = "metacritic"
# n_group = 3
# x10 = True
# stdev_factor = 1


# folder = "./data/playstore/archive_combined/"

# files = [
#     folder + "result_database.android.3.playstore.json.action.csv",
#     folder + "result_database.android.3.playstore.json.adventure.csv",
#     folder + "result_database.android.3.playstore.json.roleplaying.csv",
#     folder + "result_database.android.3.playstore.json.racing.csv",
#     folder + "result_database.android.3.playstore.json.strategy.csv",
#     folder + "result_database.android.3.playstore.json.simulation.csv",

#     folder + "result_database.android.3.playstore.json.sports.csv",
#     folder + "result_database.android.3.playstore.json.educational.csv",
#     folder + "result_database.android.3.playstore.json.puzzle.csv"
# ]

# names = [
#     "Action",
#     "Adventure",
#     "RPG",
#     "Racing",
#     "Strategy",
#     "Simulation",
#     "Sports",
#     "Educational",
#     "Puzzle"
# ]

# platform = "android"
# title = "Play Store"
# n_group = 2
# x10 = False
# stdev_factor = 3

top_limit = None

# top_limit = 1000
# top_limit = 100

plot_scores = True
plot_scores = False

min_score = None
min_score = 80
# min_score = 70
# min_score = 65

# min_score = 4

use_limits = False
use_limits = True

# top_limit_group_vect = [None, 1, 2, 3, 5, 10, 100]

top_limit_group_vect = [None]
# top_limit_group_vect = [1]

if min_score is not None:
    title += " / score " + str(min_score) + "+"


for top_limit_group in top_limit_group_vect:
    # top_limit_group = None
    # top_limit_group = 10

    # top 10 pe perioada (grup)

    if plot_scores:
        filename = "./figs/scores_per_year_" + platform + "_combined"
    else:
        filename = "./figs/titles_per_year_" + platform + "_combined"

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

        # user score!
        d["score"] = d["user_score"]

        d["score"] = d["score"].apply(lambda e: loader.get_score(e, x10))

        filter = d["score"] != "tbd"
        d = d[filter]

        if min_score is not None:
            filter = d["score"].apply(
                lambda e: e >= min_score)
            d = d[filter]

        # filter = d["release_date"].apply(
        #     lambda e: int(e.split("-")[0])) != 2020

        d = d[filter]

        d = d.sort_values(by=['score'], ascending=False)

        if top_limit is not None:
            d = d[:top_limit]

        print(len(d))

        # quit()

        if plot_scores:
            years, scores = loader.load_score_per_year(
                d, "metacritic", names[i], top_limit_group)
        else:
            years, scores = loader.load_titles_per_year(d, "metacritic", names[i])

        # print("scores: ", scores)
        # years_all = set()
  
        if not got_years:
            got_years = True
            years_all = set(years)
        else:
            for y in years:
                years_all.add(y)
            print(years_all)
            # print(set(years))

        data.append(d)
        scores_vect.append(scores)
        years_vect.append(years)

    years_all = list(years_all)
    years_all.sort()

    print(years_all)
    # quit()
    # assign all to correct years index
    # some years might be missing from some datasets (interpolate required)
    scores_vect_processed = []

    for i in range(len(files)):
        scores_processed = []
        # for all years in combined dataset
        for j, y in enumerate(years_all):
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

        print("file: " + files[i])
        # group by 5
        print(scores_processed)

    # group by 5
    print(scores_vect_processed)
    print(len(scores_vect_processed))
    print(len(scores_vect_processed[0]))
    # quit()

    scores_vect_processed_grouped = []
    years_grouped = []

    # quit()
    i_group = 0
    group_count = 0
    avg_score = 0
    year_start = 0
    year_end = 0

    year_start = str(years_all[0])

    print(years_all)

    # quit()

    # n_group = 5

    if n_group == 1:
        years_grouped = ["" + str(y) for y in years_all]
    else:
        r = len(years_all) / n_group
        rm = len(years_all) % n_group
        # print(rm)
        # quit()

        for j in range(int(r)):
            start_year = years_all[j*n_group]
            end_year = years_all[j*n_group + n_group-1]
            if j == int(r)-1 and rm != 0:
                end_year += rm
            years_grouped.append(str(start_year) + "-" + str(end_year))

        # for j, y in enumerate(years_all):
        #     i_group += 1
        #     if i_group >= n_group or j == len(years_all):
        #         i_group = 0
        #         year_end = y
        #         # year_start += 1
        #         years_grouped.append(str(year_start) + "-" + str(year_end))
        #         year_start = y

    print(years_grouped)
    # quit()
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

    plt.rc('axes', axisbelow=True)

    if plot_scores:
        # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
        #                          "Scores", years_grouped, [60,80], True, None, 0, None)
        # fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Average score",
        #                          "Average game scores by year (metacritic)", years_grouped, [60, 90], True, None, 0, None)

        fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Average score",
                                          "Average game scores by year (" +
                                          title + ")", years_grouped,
                                          [avg_score_disp-stdev_score_disp*stdev_factor, avg_score_disp +
                                              stdev_score_disp*stdev_factor] if use_limits else None,
                                          True, None, 0, None)

        fig.savefig(filename, dpi=300)

        # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
        #                          "Scores", years_grouped, None, True, None, 0, None)

        # [0,100]
    else:
        # fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Number of titles",
        #                                   "Number of titles by year (metacritic)", years_grouped, [avg_score_disp-stdev_score_disp, avg_score_disp+stdev_score_disp], True, None, 0, None)

        fig, _ = plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Number of titles",
                                          "Number of titles by year (" + title + ")", years_grouped, None, True, None, 0, None)

        fig.savefig(filename, dpi=300)
        # plot_barchart_multi_core(scores_vect_processed_grouped, color_scheme, names, "Year", "Score",
        #                          "Title", years_grouped, [0, 40], True, None, 0, None)
