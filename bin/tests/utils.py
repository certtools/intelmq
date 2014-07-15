import yaml

def get_bots_available():
    f=open('settings.cfg')
    return yaml.load(f)

def choose_bots_type(bots_list):
    count = 0
    for item in bots_list['inputs']:
        print "[%s] %s" % (count, item)
        count += 1
    raw_input()


bots_list = get_bots_available()
choose_bots_type(bots_list)
