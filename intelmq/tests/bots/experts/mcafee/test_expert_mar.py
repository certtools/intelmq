import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.experts.mcafee.expert_mar
