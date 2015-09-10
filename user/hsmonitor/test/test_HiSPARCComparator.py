import sys
sys.path.append("..")
import unittest

from HiSPARCComparator import HiSPARCComparator

from load_message import load_hisparc_message


class TestHiSPARCSingles(unittest.TestCase):

    def test_singles(self):
        comparator = load_hisparc_message('test_data/Comparator.txt')
        hisparccomparator = HiSPARCComparator([4, comparator])
        hisparccomparator.uploadCode = 'CMP'
        comparatordata = hisparccomparator.parseMessage()


if __name__ == '__main__':
    unittest.main()
