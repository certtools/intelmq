import os
#  import unittest

#  import intelmq.lib.test as test
if os.environ.get('INTELMQ_TEST_EXOTIC'):
    from intelmq.bots.outputs.misp.output_api import MISPAPIOutputBot  # noqa

# This file is a stub
# We cannot do much more as we are missing a mock MISP instance to use
# to initialise pymisp
