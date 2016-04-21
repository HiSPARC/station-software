import sys
sys.path.append("..")
import unittest

from HiSPARCComparator import HiSPARCComparator

from parse_and_check import parse_and_check_data
from load_message import load_hisparc_message


class TestHiSPARCSingles(unittest.TestCase):

    def test_singles(self):
        comparator = load_hisparc_message('test_data/Comparator.txt')
        parse_and_check_data(self, comparator, 4, HiSPARCComparator, 'CMP')


if __name__ == '__main__':
    unittest.main()
