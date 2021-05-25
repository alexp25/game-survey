import pandas as pd
df = pd.read_csv('Google-Playstore.csv')
# sort the data frame by column name
# df = df.sort_values(by="release_year")
categories = df["Category"]
categories = list(categories)
categories = list(set(categories))
print(categories)

n_titles = len(categories)
with open("categories.txt", "w", encoding="utf-8") as f:
    for i in range(n_titles):
        try:
            f.write(categories[i] + "\n")
        except:
            pass