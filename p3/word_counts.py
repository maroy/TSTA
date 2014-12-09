import re
import sys


class WordInfo:

    def __init__(self, word, doc_idx):
        self.word = word
        self.docs = set([doc_idx])

word_counts = {}

with open('text/day_11-06.txt', 'rb') as f:
    lines = f.readlines()

print 'file read'

ws = re.compile(r'\s+')

stop_words = ['nba','nfl']
sw = re.compile(r'\b' + r'\b|\b'.join(stop_words) + r'\b')

for idx in range(0, len(lines)):
    line = lines[idx]
    _, words = line.split(':')
    words = words.strip()
    words = ws.sub('', words)
    words = sw.sub(' ', words)
    for word in [w.strip() for w in words.split(' ')]:
        if word in word_counts:
            word_counts[word].docs.add(idx)
        else:
            word_counts[word] = WordInfo(word, idx)

print 'counts collected'

in_order = sorted(word_counts, lambda l, r: cmp(len(word_counts[r].docs), len(word_counts[l].docs)))

print 'sorted'

for word in in_order[:3]:
    with open('out_' + word + '.csv', 'wb') as f:
        for idx in word_counts[word].docs:
            f.write(lines[idx])

print 'files written'