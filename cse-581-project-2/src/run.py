import os

base_path = '/home/maroy/CSE-581-Project-2/src/output/'

def read_file(path):
    with open(path, 'rb') as f:
        return "".join(f.readlines())

limits = []
for d in range(5,30):
    for h in range(0,24):
        for m in range(0,60,15):
            limits.append(unicode("2014-11-%02d %02d:%02d:00" % (d, h, m)))

limits = [limit for limit in limits if limit >= '2014-11-05 22:45:00']

limit_idx = limits.index('2014-11-06 00:00:00')

done = False

while limit_idx < len(limits) and not done:
    for keyword_set in ['nba', 'nfl', 'nhl', 'any']:
        paths = [
            base_path + limits[limit_idx-3] + ' ' + keyword_set + '.txt',
            base_path + limits[limit_idx-2] + ' ' + keyword_set + '.txt',
            base_path + limits[limit_idx-1] + ' ' + keyword_set + '.txt',
            base_path + limits[limit_idx] + ' ' + keyword_set + '.txt'
        ]

        if not os.path.isfile(paths[3]):
            done = True
            break

        contents = ""
        lengths = []
        for path in paths:
            contents += read_file(path)
            lengths.append(len(contents))

        print limits[limit_idx], keyword_set, lengths
    limit_idx += 1