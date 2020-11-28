import matplotlib.pyplot as plt
import csv
import pandas as pd
import json
from modules import loader, plotter


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)


top_limit = None
# top_limit = 100

for k, thread in enumerate(config["threads"]):
    print("thread: " + str(k) + "/" + str(len(config["threads"])))

    folder = thread["out_folder"]

    class_data = loader.load_class_data(folder + "/class_data.csv")
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

    plotter.plot_score_per_year(class_data, title, class_name, top_limit)
    plotter.plot_titles_per_year(class_data, title, class_name, top_limit)
