import sys
import json
import dateutil.parser

NEXT_TREND_INDEX = 1

class Run:

    def __init__(self, map):
        self.start, self.end = [dateutil.parser.parse(part) for part in map["date"].split(' - ')]
        self.clusters = [Cluster(c) for c in map["clusters"]]


class Cluster:

    def __init__(self, arr):
        self.percentage = arr[0]
        self.words = {w: 1 for w in arr[1:]}

    def __repr__(self):
        return str(self.percentage) + ": " + ",".join(self.words)


class Trend:

    def __init__(self, cluster):

        global NEXT_TREND_INDEX

        self.accumulated_percentage = cluster.percentage
        self.cluster_count = 1

        self.unseen_count = 0
        self.words = []
        self.scores = []
        self.add(cluster)

        self.id = NEXT_TREND_INDEX
        NEXT_TREND_INDEX += 1

    def score(self, words):
        accumulated = 0
        score = 10
        top_5 = [x[0] for x in self.top(5)]
        for w in words:
            if w in top_5:
                i = self.words.index(w)
                accumulated += self.scores[i] + score
            score -= 1
        return accumulated

    def get_percentage(self):
        return self.accumulated_percentage / float(self.cluster_count)

    def unseen():
        self.unseen_count += 1
        self.cluster_count += 1

    def add(self, cluster):
        self.unseen_count = 0
        self.accumulated_percentage += cluster.percentage
        self.cluster_count += 1

        old_scores = self.scores[0:]

        score = 10
        for w in cluster.words:
            if w in self.words:
                i = self.words.index(w)
                self.scores[i] += score
            else:
                self.words.append(w)
                self.scores.append(score)
            score -= 1

        for i in range(0,len(old_scores)):
            if old_scores[i] == self.scores[i]:
                self.scores[i] *= 0.8 

    def top(self, limit):
        scores = self.scores[0:]

        top = []
        for i in range(0,limit):
            m = max(scores)
            idx = scores.index(m)
            top.append((self.words[idx], self.scores[idx]))
            scores[idx] = -1
        return top

def create_output_record(run, trends):
    record = {}
    record["start"] = str(run.start)
    record["end"] = str(run.end)

    sorted_trends = sorted(trends, lambda l, r: cmp(r.get_percentage(), l.get_percentage()))
    record["trends"] = []

    for t in sorted_trends[:3]:
        record["trends"].append({
            "id": t.id,
            "score": t.get_percentage(),
            "words": [top[0] for top in t.top(10)]
        })

    return record

# def output_top(trends, count):

#     sorted_trends = sorted(trends, lambda l, r: cmp(r.get_percentage(), l.get_percentage()))

#     print ",".join([t.top(1)[0][0] + ":" + str(t.get_percentage()) for t in sorted_trends[:3]])


def main():
    MIN_SCORE = 0

    output = []

    with open(sys.argv[1]) as f:
        runs = [Run(r) for r in json.load(f)]

    trends = []

    for r in range(0, len(runs)):
        trends_copy = trends[0:]
        run = runs[r]
        for c in run.clusters:
            top_score = 0
            top_idx = -1
            for i in range(0, len(trends)):
                t = trends[i]
                score = t.score(c.words)
                if score > top_score:
                    top_score = score
                    top_idx = i
            if top_score > MIN_SCORE:
                if top_idx < len(trends_copy):
                    trends_copy[top_idx] = None
                trends[top_idx].add(c)
            else:
                trends.append(Trend(c))
        for t in trends_copy:
            if t is not None:
                if t.unseen_count > 4:
                    trends.remove(t)
                else:
                    t.unseen_count += 1
        # output_top(trends, 3)
        output.append(create_output_record(run, trends))

    with open(sys.argv[2], "wb") as f:
        json.dump(output, f)

if __name__ == "__main__":
    main()