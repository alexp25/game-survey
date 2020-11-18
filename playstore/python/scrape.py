import play_scraper
# print(play_scraper.collection(
#         collection='TRENDING',
#         category='GAME_RACING',
#         results=5,
#         page=1))

categories = play_scraper.categories()

for category in categories:
    print(category)
    print(categories[category])


print("scrape collection")

print(play_scraper.collection(
        collection='TOP_FREE',
        # category='GAME_RACING',
        results=50,
        page=10))