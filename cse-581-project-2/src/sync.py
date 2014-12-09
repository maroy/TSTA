import os
import sys
import glob
import shutil

_from = sys.argv[1]
_to = sys.argv[2]

print _from, _to

for file in glob.glob1(_from, "2014*.db"):
    from_file = os.path.join(_from, file)
    to_file = os.path.join(_to, file)

    if not os.path.isfile(to_file):
        print "copy file {0} => {1}".format(from_file, to_file)

