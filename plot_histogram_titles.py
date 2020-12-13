
import csv
import pandas as pd
from modules.graph import plot_barchart_multi_core
import numpy as np
from modules import loader
from matplotlib import pyplot as plt
from modules.graph import plot_barchart_multi_core, set_rotation
import math 
import json

folder = "./data/googlescholar/"

files = [
    folder + "result_database.blockchain.json.csv",
    folder + "result_database.crowdsensing.json.csv",
    folder + "result_database.serious_gaming.json.csv",
    folder + "result_database.crowdsensing_blockchain.json.csv",
    folder + "result_database_2.urban_water.json.csv",
    folder + "result_database_2.blockchain_water.json.csv",
    folder + "result_database_2.crowdsensing_water.json.csv"
]

names = [
    "Blockchain",
    "Crowdsensing",
    "Serious Gaming",
    "Crowdsensing+Blockchain",
    "Urban Water",
    "Blockchain+Water",
    "Crowdsensing+Water"
]

# very slow
postprocessing_keywords = True
# load processed
load = True

exclude = ["for", "in", "a", "an", "the", "and", "of", "to", "on", "with", "", "[pdf][pdf]", "[html][html]"]

titles_all = []


def process(dict_keywords, exclude):
    kwp = []
    for key, value in dict_keywords.items():
        # key = key.lower()
        kwp.append([key, value])

    kwp = [kw for kw in kwp if kw[0] not in exclude]

    kwp.sort(key=lambda kw: kw[1], reverse=True)
    return kwp

for i in range(len(files)):
    d = loader.load_class_data(files[i])
    titles = list(d["title"])
    titles_all.extend(titles)

dict_keywords = {}
for i in range(len(titles_all)):
    title = titles_all[i]
    kws = title.split(" ")
    for i, kw in enumerate(kws): 
        kw = kw.lower()
        # check word
        if kw not in dict_keywords:
            dict_keywords[kw] = 1
        else:
            dict_keywords[kw] += 1
        # check combination of 2 words
        if i < len(kws) - 1:
            kw = kw + " " + kws[i+1].lower()
        if kw not in dict_keywords:
            dict_keywords[kw] = 1
        else:
            dict_keywords[kw] += 1

kwp = process(dict_keywords, exclude)

with open("kw_init.txt", "w") as f:
    f.write(json.dumps(kwp))

# quit()

# trim keywords
# if separate keywords are found in a group, remove the separate ones

print(len(dict_keywords))

if postprocessing_keywords and not load:
    dict_keywords_trim = {}
    counter = 0
    for key1, value1 in kwp:
        add_single = True
        print("kw " + str(counter))
        counter += 1
        for key2, value2 in kwp:
            # group found, remove key1, use group
            if (key2.find(key1) != -1) and (len(key2) > len(key1)):
                add_single = False
                dict_keywords_trim[key2] = value2
                break
        if add_single:
            dict_keywords_trim[key1] = value1
                
    dict_keywords = dict_keywords_trim

kwp = []
if not load:
    kwp = process(dict_keywords, exclude)

    with open("kw_proc.txt", "w") as f:
        f.write(json.dumps(kwp))
else:
    with open("kw_proc.txt", "r") as f:
        kwp = json.loads(f.read())

# quit()
# plt.hist(dict_keywords)

keys = []
values = []

avg_count = math.ceil(sum([kw[1] for kw in kwp])/len(kwp))
print(avg_count)
kwp = [kw for kw in kwp if kw[1] > avg_count]

print(len(kwp))

# quit()
print(kwp)
kwp = kwp[:5]
# kwp = [kwp[0], kwp[3], kwp[5], kwp[6], kwp[7]]

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