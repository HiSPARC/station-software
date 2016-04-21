import sys
sys.path.append("..")
import unittest

from HiSPARCError import HiSPARCError

from parse_and_check import parse_and_check_data
from load_message import load_hisparc_message


class TestHiSPARCError(unittest.TestCase):

    def test_error(self):
        error = load_hisparc_message('test_data/Error.txt')
        parse_and_check_data(self, error, 2, HiSPARCError, 'ERR')


if __name__ == '__main__':
    unittest.main()
