import matplotlib.pyplot as plt
import csv
import pandas as pd
import json
import math
from modules import loader, plotter, utils
import sys

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if len(sys.argv) == 1:
    platform = 1
    min_score = None
else:
    args = sys.argv
    platform = int(args[1].split("--platform=")[1])
    min_score = int(args[2].split("--min-score=")[1])
    if min_score == 0:
        min_score = None

print(platform, min_score)


if platform == 1:
    class_data = loader.load_class_data(
        "./data/metacritic_v2/result_database.pc.json.csv")
    class_name = "PC"
    title = "PC"
    x10 = True
elif platform == 2:
    class_data = loader.load_class_data(
        "./data/metacritic_v2/result_database.console.json.csv")
    class_name = "console"
    title = "console"
    x10 = True
elif platform == 3:
    class_data = loader.load_class_data(
        "./data/playstore/archive_combined/result_database.android.3.playstore.json.csv")
    class_name = "android"
    title = "Play Store"
    x10 = False
elif platform == 4:
    class_data = loader.load_class_data("./data/metacritic_v2/result_database.json.csv")
    class_name = "ios"
    title = "iOS"
    x10 = False


top_limit = None
# top_limit = 100


# user score!
class_data["score"] = class_data["user_score"]
filter = class_data["user_score"] != "tbd"
class_data = class_data[filter]
class_data = class_data.sort_values(by=['user_score'], ascending=False)

if top_limit is not None:
    class_data = class_data[:top_limit]

if min_score is not None:
    class_data["temp_score"] = class_data["score"].apply(lambda e: loader.get_score(e, x10))
    class_data = class_data[class_data['temp_score'] >= min_score]

# print(class_data)

if top_limit is not None:
    title += " top " + str(top_limit)
    class_name += " top " + str(top_limit)

if min_score is not None:
    title += " / score " + str(min_score) + "+"
    class_name += "_" + str(min_score)

plt.rc('axes', axisbelow=True)


plotter.plot_score_per_year(class_data, title, class_name, x10)
plotter.plot_titles_per_year(class_data, title, class_name, x10)
