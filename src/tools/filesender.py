import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib.pipeline import Pipeline
from lib.utils import force_decode

file = open(sys.argv[1], 'r')
pipeline = Pipeline(None, [sys.argv[2]])

for line in file:
    line = force_decode(line)
    pipeline.send(line)

file.close()
