# count_lines.py

import os

path = '/home/maroy/CSE-581-Project-2/src/output/'

counts = {'nba': 0, 'nfl': 0, 'nhl': 0, 'any': 0}

(_, _, filenames) = os.walk(path).next()

for fn in filenames:
    with open(path + fn, 'rb') as f:
        count = len(f.readlines())
        for k in counts:
            if k in fn:
                counts[k] += count

print counts