import csv
from dateutil import parser
import datetime
import json
import traceback


# 1. Half-Life 2
# 96
# User: 9.1
# "Release Date: Nov 16, 2004"


# Half-Life 2
# 96
# User:
# 9.1
# Release Date:
# Nov 16, 2004

# 25 to Life
# 39,25
# Release Date:
# Jan 17


# 1623.
# Starship Troopers
# November 15, 2005
# User Score
# 6.1

def extract_metacritic_5(filename):
    entries = []
    with open(filename, 'r', encoding="utf-8") as f:
        data = f.read()
        data = data.split("\n")
        data = [e for e in data if len(e) > 0]
        n_entries = len(data) / 5
        print("n_entries: ", n_entries)
        n_entries = int(n_entries)
        for i in range(n_entries):
            try:
                entry = []
                # entry.append(data[i*4+0].replace("\"",
                #                                  "").split(".")[1].lstrip())
                # entry.append(data[i*4+1].replace("\"", "").lstrip())
                # entry.append(data[i*4+2].replace("\"",
                #                                  "").split(":")[1].lstrip())
                # entry.append(data[i*4+3].replace("\"",
                #                                  "").split(":")[1].lstrip())

                # 1015,Age of Empires III: The WarChiefs,80,7.8,2006-10-17


                if data[i*5+2] == 'tbd':
                    continue


                entry.append(data[i*5+1])
                entry.append(data[i*5+4])
                entry.append(data[i*5+4])

                date = data[i*5+2]
                date = date.split(" ")
                date[0] = date[0][:3]
                date = " ".join(date)

                entry.append(date)

                # November 15, 2005               


                for j, e in enumerate(entry):
                    entry[j] = e.replace(",", "")
                entries.append(entry)
            except:
                print("exception at: ", data[i*5+1])
                traceback.print_exc()             
                pass
    return entries


def extract_metacritic(filename):
    entries = []
    with open(filename, 'r', encoding="utf-8") as f:
        data = f.read()
        data = data.split("\n")
        data = [e for e in data if len(e) > 0]
        n_entries = len(data) / 6
        print("n_entries: ", n_entries)
        n_entries = int(n_entries)
        for i in range(n_entries):
            try:
                entry = []
                # entry.append(data[i*4+0].replace("\"",
                #                                  "").split(".")[1].lstrip())
                # entry.append(data[i*4+1].replace("\"", "").lstrip())
                # entry.append(data[i*4+2].replace("\"",
                #                                  "").split(":")[1].lstrip())
                # entry.append(data[i*4+3].replace("\"",
                #                                  "").split(":")[1].lstrip())

                entry.append(data[i*6+0])
                entry.append(data[i*6+1])
                entry.append(data[i*6+3])
                entry.append(data[i*6+5])

                for j, e in enumerate(entry):
                    entry[j] = e.replace(",", "")

                entries.append(entry)
            except:
                print("exception at: ", data[i*6])
                pass
    return entries


def save_class_data(filename, entries):
    class_data = ""
    rank = 1
    class_data += "rank,title,score,user_score,release_date\n"
    for e in entries:
        try:
            format_str = '%b %d %Y'
            class_data += str(rank) + "," + e[0] + "," + e[1] + "," + e[2] + "," + str(
                datetime.datetime.strptime(e[3], format_str).date()) + "\n"
        except:
            print("exception at: " + e[0])
            traceback.print_exc()
        rank += 1
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(class_data)
    return class_data


with open("config.json", "r") as f:
    config = f.read()
    config = json.loads(config)

for k, thread in enumerate(config["threads"]):
    print("thread: " + str(k) + "/" + str(len(config["threads"])))

    folder = thread["out_folder"]
    entries = []
    for i in range(0, 100):
        try:
            data = extract_metacritic_5(folder + "/" + "page" + str(i) + ".csv")
            entries.extend(data)
        except:
            print("exception at index: " + str(i))

    for e in entries:
        print(e)

    print(len(entries))

    class_data = save_class_data(folder + "/class_data.csv", entries)
    print(class_data)

    print(len(entries))
