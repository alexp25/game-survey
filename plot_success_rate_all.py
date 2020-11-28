import csv
import numpy as np
import matplotlib
from modules.graph import plot_barchart_multi_core
from statistics import stdev
import matplotlib.pyplot as plt


def read_csv_2d(filename):
    with open(filename, "r") as f:
        data = csv.reader(f, delimiter=',')
        # return [float(d[0]) for d in data]
        return [[float(d) for d in row] for row in data]

def read_csv_1d(filename):
    with open(filename, "r") as f:
        data = csv.reader(f, delimiter=',')
        return [d for d in data]

def get_percent(d1, d2):
    
    print(d1)
    print(d2)

    s = np.shape(d1)
    sr = np.zeros(s)

    for i in range(s[0]):
        for j in range(s[1]):
            print(i,j)
            if d1[i][j] > 0:
                sr[i][j] = int(d2[i][j] / d1[i][j] * 100)
            else:
                sr[i][j] = 0

    return sr
        

all_titles = read_csv_2d("./figs/titles_per_year_all_user.png.1.csv")
top_titles = read_csv_2d("./figs/titles_per_year_all_user_80.png.1.csv")
years = read_csv_1d("./figs/years_all_user.png.1.csv")

names = ["Action", "Adventure", "RPG",
         "FPS", "Racing", "RTS", "Simulation", "Third Person"]

source = "Metacritic"
label = "all_user"

print(all_titles)
print(top_titles)
print(years)

success_rate = get_percent(np.array(all_titles), np.array(top_titles))
print(success_rate)

success_rate = success_rate[0]
years = [int(y) for y in years[0]]
years = dict((el,0) for el in years).keys()

print(years)

# plt.bar(score_per_year)
# color='blue'
plt.bar(years, success_rate)
plt.xlabel("Year")
plt.ylabel("Success rate [%]")
plt.title("Success rate by year (" + source + ")")

delta = (max(success_rate) - min(success_rate))/10
plt.ylim([min(success_rate) - delta, max(success_rate) + delta])

# plt.ylim([0, 100])
# plt.xticks(years, success_rate)
# plt.xticks([])  # Disable xticks.
plt.legend([label])

# plt.xticks(np.arange(min(years), max(years)+1, 1))


fig = plt.gcf()
fig.savefig("./figs/success_rate_by_year_1.png", dpi=300)

plt.show()
