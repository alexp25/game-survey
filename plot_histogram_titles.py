
import csv
import pandas as pd
from modules.graph import plot_barchart_multi_core
import numpy as np
from modules import loader
from matplotlib import pyplot as plt
from modules.graph import plot_barchart_multi_core, set_rotation
import math 

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

titles_all = []

for i in range(len(files)):
    d = loader.load_class_data(files[i])
    titles = list(d["title"])
    titles_all.extend(titles)

dict_keywords = {}
for i in range(len(titles_all)):
    title = titles_all[i]
    kws = title.split(" ")
    for kw in kws: 
        kw = kw.lower()
        if kw not in dict_keywords:
            dict_keywords[kw] = 1
        else:
            dict_keywords[kw] += 1


# plt.hist(dict_keywords)
kwp = []

keys = []
values = []

exclude = ["for", "in", "a", "the", "and", "of", "to", "on", "with", "", "[pdf][pdf]"]

for key, value in dict_keywords.items():
    # key = key.lower()
    kwp.append([key, value])

kwp = [kw for kw in kwp if kw[0] not in exclude]

kwp.sort(key=lambda kw: kw[1], reverse=True)
avg_count = math.ceil(sum([kw[1] for kw in kwp])/len(kwp))
print(avg_count)
kwp = [kw for kw in kwp if kw[1] > avg_count]

print(len(kwp))

# quit()

kwp = kwp[:5]

print(kwp)

for kw in kwp:
    keys.append(kw[0])
    values.append(kw[1])


# print(keys, values)
filename = "./figs/histogram_keywords"

# set_rotation(90)

fig, _ = plot_barchart_multi_core([values], None, ["all"], "", "Count",
                                          "Title keywords", keys, None, True, 0, 0, None)
fig.savefig(filename, dpi=300)
# print(dict_keywords)