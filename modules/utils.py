def downsample_list(rows, n, from_top):
    n_rows = len(rows)
    skip = int(n_rows / n) + 1
    new_list = []
    i = 0
    while True:
        index = i*skip
        if index < n_rows:
            new_list.append(rows[i*skip])
        else:
            break
        i = i + 1
    return new_list

def downsample_list_divn(rows, n):
    new_list = []
    for i in range(len(rows)):
        if i % n == 0:
            new_list.append(rows[i])
    return new_list