# Health & Fitness
# Travel & Local

import pandas as pd

# rank,title,score,user_score,release_date,category

category = "Health & Fitness"
file_name = "health_fitness"

# category = "Travel & Local"
# file_name = "travel_local"

df = pd.read_csv('Google-Playstore.csv')

# sort the data frame by column name
# df = df.sort_values(by="release_year")
is_category = df['Category'] == category
df = df[is_category]
# print(df)
df = df.rename(columns={'Category': 'category', 'Rating': 'score',
                        "Released": "release_date", "App Name": "title"})
result = df.sort_values(['score'], ascending=[1])
df["rank"] = range(1, len(df) + 1)
df["user_score"] = df["score"]
result = df.sort_values(['release_date'], ascending=[1])


def get_year(x):
    year = 0
    try:
        year = int(x.split(",")[1])
    except:
        pass
    return year


df["release_date"] = df["release_date"].apply(lambda x: get_year(x))
df = df[df["release_date"] != 0]
df = df[['rank', 'title', 'score', 'user_score', 'release_date', 'category']]

df.to_csv(file_name + ".csv", index=False, header=True)
