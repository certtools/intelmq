import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.outputs.mcafee.output_esm_ip
