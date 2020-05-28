import csv
import numpy as np
import matplotlib
from graph import plot_barchart_multi_core
from statistics import stdev

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
        

all_titles = read_csv_2d("./figs/titles_per_year_combined.png.csv")
top_titles = read_csv_2d("./figs/titles_per_year_combined_over_80.png.csv")
years_grouped = read_csv_1d("./figs/titles_per_year_combined.png.years.csv")

names = ["Action", "Adventure", "RPG",
         "FPS", "Racing", "RTS", "Simulation", "Third Person"]

print(all_titles)
print(top_titles)

success_rate = get_percent(np.array(all_titles), np.array(top_titles))

print(success_rate)

years_grouped = years_grouped[0]
print(years_grouped)


cmap = matplotlib.cm.get_cmap('viridis')
color_scheme = [cmap(i) for i in np.linspace(0, 1, len(names))]
print(color_scheme)


 # get avg and stdev for all
all_scores_disp = []
for g in success_rate:
    for e in g:
        all_scores_disp.append(e)

avg_score_disp = sum(all_scores_disp)/len(all_scores_disp)
stdev_score_disp = stdev(all_scores_disp)

fig, _ = plot_barchart_multi_core(success_rate, color_scheme, names, "Year", "Success rate [%]",
                                          "Success rate by year (metacritic)", years_grouped, [avg_score_disp-stdev_score_disp, avg_score_disp+stdev_score_disp], True, None, 0, None)

fig.savefig("./figs/success_rate_by_year.png", dpi=300)