"""
Tests the upgrade functions.
"""
import unittest

import intelmq.lib.upgrades as upgrades


def generate_function(function):
    def test_function(self):
        """ Test if no errors happen for upgrade function %s. """ % function.__name__
        function({}, {}, dry_run=True)
    return test_function


class TestUpgradeLib(unittest.TestCase):
    def setUp(self):
        self.allfs = upgrades.__all__
        self.modulefs = [f for f in dir(upgrades) if f.startswith('v')]
        self.mapping_list = []
        self.mapping_list_name = []
        for values in upgrades.UPGRADES.values():
            self.mapping_list.extend((x for x in values))
            self.mapping_list_name.extend((x.__name__ for x in values))


    def test_all_functions_used(self):
        self.assertEqual(len(self.mapping_list_name),
                         len(set(self.mapping_list_name)),
                         msg='Some function is assigned to multiple versions.')
        self.assertEqual(set(self.allfs),
                         set(self.mapping_list_name),
                         msg='v* functions in the module do not '
                             'match the mapping.')
        self.assertEqual(set(self.allfs), set(self.modulefs),
                         msg='v* functions in the module do not '
                             'match functions in __all__.')


for name in upgrades.__all__:
    setattr(TestUpgradeLib, 'test_function_%s' % name,
            generate_function(getattr(upgrades, name)))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
