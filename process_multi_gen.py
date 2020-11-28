import matplotlib.pyplot as plt
import csv
import pandas as pd
import json
import math
from modules import loader, plotter

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


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)


top_limit = None
# top_limit = 100

top_score = None
# top_score = 80
top_score = 4


class_data = loader.load_class_data(
    "./data/playstore/archive_combined/result_database.android.3.playstore.json.csv")
class_name = "android"
title = "android"
x10 = False

# class_data = loader.load_class_data("./data/metacritic_v2/result_database.json.csv")
# class_name = "ios"
# title = "iOS"
# x10 = False

# class_data = loader.load_class_data(
#     "./data/metacritic_v2/result_database.console.json.csv")
# class_name = "console"
# title = "console"
# x10 = True

# class_data = loader.load_class_data(
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
    class_data["temp_score"] = class_data["score"].apply(lambda e: loader.get_score(e, x10))
    class_data = class_data[class_data['temp_score'] >= top_score]

# print(class_data)

if top_limit is not None:
    title += " top " + str(top_limit)
    class_name += " top " + str(top_limit)

if top_score is not None:
    title += " / score " + str(top_score) + "+"
    class_name += "_" + str(top_score)

plt.rc('axes', axisbelow=True)


plotter.plot_titles_per_year(class_data, title, class_name, x10)
# plotter.plot_titles_per_year(class_data, title, class_name)
