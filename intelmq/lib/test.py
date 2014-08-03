from event import Event
from sanitize import *

e = Event()
e = generate_source_time(e, "source_time")
e = generate_observation_time(e, "observation_time")
print e

