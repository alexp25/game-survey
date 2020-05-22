import csv
from dateutil import parser
import datetime


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


# 1.
# Half-Life 2
# Platform:
# PC
# November 16, 2004
# [Metacritic's 2004 PC Game of the Year]  By taking the suspense, challenge and visceral charge of the original, and adding startling new realism and responsiveness, Half-Life 2 opens the door to a world where the player's presence affects everything around him, from the physical environment to the behaviors -- even the emotions -- of both friends and enemies. The player again picks up the crowbar of research scientist Gordon Freeman, who finds himself on an alien-infested Earth being picked to the bone, its resources depleted, its populace dwindling. Freeman is thrust into the unenviable role of rescuing the world from the wrong he unleashed back at Black Mesa. And a lot of people -- people he cares about -- are counting on him. [Vivendi Universal]
# User Score
# 9.1
# Expand
# 96

def extract_metacritic_4(filename):
    entries = []
    with open(filename, 'r') as f:
        data = f.read()
        data = data.split("\n")
        data = [e for e in data if len(e) > 0]
        n_entries = len(data) / 4
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

                entry.append(data[i*4+0])
                scores = data[i*4+1].split(",")
                entry.append(scores[0])
                entry.append(scores[1])
                entry.append(data[i*4+3])
                if scores[1] == 'tbd':
                    continue
                for j, e in enumerate(entry):
                    entry[j] = e.replace(",", "")
                entries.append(entry)
            except:
                print("exception at: ", data[i*4])
                pass
    return entries


def extract_metacritic(filename):
    entries = []
    with open(filename, 'r') as f:
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
        rank += 1
    with open(filename, 'w') as f:
        f.write(class_data)
    return class_data


folder = "./data/metacritic"
entries = []
for i in range(0, 100):
    try:
        data = extract_metacritic(folder + "/" + "page" + str(i) + ".csv")
        entries.extend(data)
    except:
        print("exception at index: " + str(i))

for e in entries:
    print(e)

print(len(entries))

class_data = save_class_data(folder + "/class_data.csv", entries)
print(class_data)

print(len(entries))
