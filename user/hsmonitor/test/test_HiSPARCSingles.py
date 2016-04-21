import sys
sys.path.append("..")
import unittest

from HiSPARCSingles import HiSPARCSingles

from parse_and_check import parse_and_check_data
from load_message import load_hisparc_message


class TestHiSPARCSingles(unittest.TestCase):

    def test_singles(self):
        singles = load_hisparc_message('test_data/Singles.txt')
        parse_and_check_data(self, singles, 5, HiSPARCSingles, 'SIN')


if __name__ == '__main__':
    unittest.main()
