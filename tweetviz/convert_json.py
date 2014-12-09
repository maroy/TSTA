import sys
import json
import dateutil.parser

class Cluster:

    def __init__(self, arr):
        self.percentage = arr[0]
        self.words = arr[1:]

    def to_map(self):
        return {
            "percentage": self.percentage,
            "words": self.words
        }
        

class ClusterRun:

    def __init__(self, map):

        date_strs = map["date"].split(" - ")

        self.start_date = dateutil.parser.parse(date_strs[0])
        self.end_date = dateutil.parser.parse(date_strs[1])

        self.clusters = []
        for c in map["clusters"]:
            self.clusters.append(Cluster(c))

    def to_map(self):
        return {
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "clusters": [c.to_map() for c in self.clusters]
        }


with open(sys.argv[1]) as f:
    input = json.load(f)

output = []

for i in input:
    output.append(ClusterRun(i).to_map())

with open(sys.argv[2], 'wb') as f:
    json.dump(output, f)