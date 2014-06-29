import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib.pipeline import Pipeline
from lib.utils import force_decode

if len(sys.argv) != 3:
    print
    print "\tUsage: python %s <input-file> <queue1,queue2..>" % sys.argv[0]
    print 
    print "\tExample: python %s /tmp/events.txt events-queue" % sys.argv[0]
    print
    exit()

file = open(sys.argv[1], 'r')

queues = sys.argv[2].split(',')

pipeline = Pipeline(None, queues)

for line in file:
    line = force_decode(line)
    pipeline.send(line)

file.close()
