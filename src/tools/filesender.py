import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib.pipeline import Pipeline
from lib.utils import force_decode

file = open(sys.argv[1], 'r')

queues = sys.argv[2].split(','):

pipeline = Pipeline(None, queues)

for line in file:
    line = force_decode(line)
    pipeline.send(line)

file.close()
