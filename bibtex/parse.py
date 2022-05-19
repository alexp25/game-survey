from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import bibtexparser
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

FSIZE_TITLE = 16
FSIZE_LABEL = 14
FSIZE_LABEL_S = 14
FSIZE_LABEL_XS = 14

remove_chars = ["{", "}", "[", "]", "\\"]

with open('refs.txt', encoding='utf-8') as bibtex_file:
    bibtex_database = bibtexparser.load(bibtex_file)
    print(bibtex_database.entries)
    years = {}
    years_list = []
    count_list = []
    titles_list = []
    for entry in bibtex_database.entries:
        if "year" in entry:
            if not entry["year"] in years:
                years[entry["year"]] = 1
            else:
                years[entry["year"]] += 1
        if "title" in entry:
            title = entry["title"]
            for rc in remove_chars:
                title = title.replace(rc, "")
            titles_list.append(title)

    years_list = list(years.keys())
    years_list.sort()
    count_list = [years[y] for y in years_list]
    years_list = [int(year) for year in years_list]
    print(years_list)
    print(count_list)

years_list_idx = []

for idx, year in enumerate(years_list):
    if year >= 2012 and year <= 2021:
        years_list_idx.append(idx)

years_list_filtered = []
count_list_filtered = []

for idx in years_list_idx:
    years_list_filtered.append(years_list[idx])
    count_list_filtered.append(count_list[idx])

years_list = years_list_filtered
count_list = count_list_filtered

print(titles_list)

# plt.figure()
# plt.bar(years_list, count_list)
# plt.xlabel("Year", fontsize=FSIZE_LABEL)
# plt.ylabel("Number of papers", fontsize=FSIZE_LABEL)
# plt.title("Number of references by year", fontsize=FSIZE_TITLE)
# delta = (max(count_list) - min(count_list))/10
# plt.ylim([min(count_list) - delta, max(count_list) + delta])
# # plt.xticks(years, scores)
# ax = plt.gca()
# # ax.grid(zorder=0)
# ax.set_axisbelow(True)
# ax.xaxis.set_major_locator(MaxNLocator(integer=True))
# ax.tick_params(axis='both', which='major', labelsize=FSIZE_LABEL_XS)
# ax.tick_params(axis='both', which='minor', labelsize=FSIZE_LABEL_XS)
# plt.legend(["References"], fontsize=FSIZE_LABEL_XS)
# fig = plt.gcf()
# fig.savefig("./references_per_year.png", dpi=300)
# plt.show()


exclude = ["for", "in", "a", "an", "the", "and", "of",
           "to", "on", "with", "", "[pdf][pdf]", "[html][html]"]

def process(dict_keywords, exclude):
    kwp = []
    for key, value in dict_keywords.items():
        # key = key.lower()
        kwp.append([key, value])

    kwp = [kw for kw in kwp if kw[0] not in exclude]

    kwp.sort(key=lambda kw: kw[1], reverse=True)
    return kwp


def get_dict_keywords(titles_all):
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
    return dict_keywords


dict_keywords = get_dict_keywords(titles_list)
kwp = process(dict_keywords, exclude)
kwp = [kw[0] for kw in kwp]

print(kwp)
# quit()

text = " ".join(titles_list)
text = " ".join(kwp)

# lower max_font_size, change the maximum number of word and lighten the background:
wordcloud = WordCloud(width=800, height=600, max_font_size=100, max_words=100,
                      background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
fig = plt.gcf()
fig.savefig("./wordcloud_reference_titles.png", dpi=300)
plt.show()
