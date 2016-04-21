import sys
sys.path.append("..")
import unittest

from HiSPARCConfig import HiSPARCConfig

from parse_and_check import parse_and_check_data
from load_message import load_hisparc_message


class TestHiSPARCConfig(unittest.TestCase):

    def test_config(self):
        config = load_hisparc_message('test_data/Config_v40.txt')
        parse_and_check_data(self, config, 3, HiSPARCConfig, 'CFG')


if __name__ == '__main__':
    unittest.main()
