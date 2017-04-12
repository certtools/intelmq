import json
import os.path
import shutil
import datetime
import collections
import pwd
import grp
import os
from conf import *

#converts the pipe data from bots:queues kvs to
#queues: bots kv
def convert_pipedata(pipe_data):
    sqs2bot = {}
    dsq_count = {}
    for bot in pipe_data:
        src_qs =  pipe_data[bot].get('source-queue','')
        src_qs =  [src_qs,]
        dst_qs =  pipe_data[bot].get('destination-queues',[])
        for q in src_qs:
            if q in sqs2bot:
                qb = sqs2bot[q]
                qb.append(q)
                sqs2bot[q] = qb
            else:
                sqs2bot[q] = [bot,]

        for q in dst_qs:
            if q in dsq_count:
                qb = dsq_count[q]
                qb += 1
                dsq_count[q] = qb
            else:
                dsq_count[q] = 1
    return (sqs2bot, dsq_count)

# Return only the bots which are directly connected
# If a bot has more than one inputs or outputs stop processing
#
def connected_bots(bot,rc_data,pipe_data):
    cbs = []
    sqs2bot, dsq_count = convert_pipedata(pipe_data)
    cbot = bot
    while True:
        dst_qs =  pipe_data[cbot].get('destination-queues',[])
        if len(dst_qs) == 1:
            dst_q = dst_qs[0]
            _bot = sqs2bot[dst_q]
            cbot = _bot[0]
            count = dsq_count[dst_q]
            if count > 1: break
            else: cbs.append(cbot)
        else:
            break
    return cbs

def main():
    with open(RUNTIME_CONF, encoding='utf-8') as rc_file:
        rc_data = json.loads(rc_file.read())

    with open(PIPELINE_CONF, encoding='utf-8') as pipe_file:
        pipe_data = json.loads(pipe_file.read())

    if not os.path.exists(SYSTEMD_OUTPUT_DIR):
            os.makedirs(SYSTEMD_OUTPUT_DIR)

    intelmq_user=INTELMQ_USER
    intelmq_group=INTELMQ_GROUP

    collectors = [i for i in rc_data if rc_data[i]['group'] == 'Collector']
    parsers = [i for i in pipe_data if rc_data[i]['group'] == 'Parser']

    for bot in collectors:
        bot_data = rc_data[bot]
        #bot_group = bot_data['group']

        cbs = connected_bots(bot,rc_data,pipe_data)

        if DISABLE_IN_CONF:
           rc_data[bot]['enabled'] = False

        if SET_RUNMODE_IN_CONF:
           rc_data[bot]['run_mode'] = 'scheduled'

        bot_parameters = bot_data['parameters']
        bot_interval = int(bot_parameters['rate_limit'])
        bot_run_cmd = INTELMQCTL_BIN+' run '+bot
        service_file_name = SYSTEMD_OUTPUT_DIR+os.path.sep+SERVICE_PREFIX+bot+'.service'
        bot_service_name = SERVICE_PREFIX+bot+'.service'
        timer_file_name = SYSTEMD_OUTPUT_DIR+os.path.sep+SERVICE_PREFIX+bot+'.timer'
        service_data = service_template.substitute(locals())
        timer_data = timer_template.substitute(locals())
        with open(service_file_name, "w", encoding='utf-8') as svc_file:
            svc_file.write(service_data)
        with open(timer_file_name, "w", encoding='utf-8') as tmr_file:
            tmr_file.write(timer_data)

    if DISABLE_IN_CONF or SET_RUNMODE_IN_CONF:
        shutil.move(RUNTIME_CONF, RUNTIME_CONF+'.bak')
        rc_data = collections.OrderedDict(sorted(rc_data.items()))
        data = json.dumps(rc_data, indent=4)
        with open(RUNTIME_CONF, "w", encoding='utf-8') as rc_file:
            rc_file.write(data)
        intelmq_uid = pwd.getpwnam(intelmq_user).pw_uid
        intelmq_gid = grp.getgrnam(intelmq_group).gr_gid
        os.chown(RUNTIME_CONF, intelmq_uid, intelmq_gid)
        os.chmod(RUNTIME_CONF, 0o664) #u-rw, g-rw (for intelmq-manager), o-r

    print(POST_DOCS)
if __name__=="__main__":
    main()
