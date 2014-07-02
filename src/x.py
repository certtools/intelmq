from lib.event import Event

event = Event()
event.add("domain name","host.com")
event.add("reverse dns","host.com.ptr")

print unicode(event)

for key in event.keys():
    value = event.value(key)
    event.clear(key)
    key = key.replace(' ','_')
    event.add(key, value)

print unicode(event)
