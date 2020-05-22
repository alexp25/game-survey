import csv
import json


# Half-Life 2
# 96
# Release Date:
# Nov 16, 2004

# add:

# User Score:
# 6.4

def merge_dates(list_file, details_file):
    with open(list_file, "r", encoding="utf-8") as lf:
        list_data = lf.read().split("\n")
    with open(details_file, "r", encoding="utf-8") as df:
        details_data = df.read().split("\n")

    n_titles = int(len(list_data)/4)
    print(n_titles)
    titles = []
    for i in range(n_titles):
        titles.append(list_data[i*4])

    dates = []
    uscores = []
    mscores = []

    skip = False

    for title in titles:
        for index, d in enumerate(details_data):
            if title == d:
                try:
                    print("found: ", title)
                    dates.append(details_data[index+1])
                    
                    for index_d in range(100):
                        if "Metascore:" in details_data[index+index_d]:
                            mscores.append(details_data[index+index_d+1])
                        if "User Score:" in details_data[index+index_d]:
                            uscores.append(details_data[index+index_d+1])
                            break
                except:
                    print("exception at index: " + str(index))
                    mscores.append(0)
                    uscores.append(0)
                    skip = True
                break
        if skip:
            continue
    print("dates: ")
    for d in dates:
        print(d)
    print(len(dates))

    print("uscores: ")
    for d in uscores:
        print(d)
    print(len(uscores))

    print("mscores: ")
    for d in mscores:
        print(d)
    print(len(mscores))

    for i, d in enumerate(dates):
        d1 = d.split(" ")
        if mscores[i] != 0 and uscores[i] != 0:
            list_data[i*4+1] = str(mscores[i]) + "," + str(uscores[i])
        list_data[i*4+3] = d1[0][:3] + " " + d1[1] + " " + d1[2]

    # for d in list_data:
    #     print(d)

    return list_data


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)

for k, thread in enumerate(config["threads"]):
    print("thread: " + str(k) + "/" + str(len(config["threads"])))

    folder = thread["out_folder"]

    for i in range(0, 100):
        try:
            print("index: " + str(i))
            data = merge_dates(folder+"/page"+str(i)+".csv",
                            folder+"/page"+str(i)+".d.csv")

            with open(folder+"/page"+str(i)+".csv", "w", encoding="utf-8") as f:
                f.write("\n".join(data))
        except FileNotFoundError:
            print("file not found at index: " + str(i))
        except UnicodeDecodeError:
            print("unicode decode error at index: " + str(i))
        except IndexError:
            print("index error at index: " + str(i))
