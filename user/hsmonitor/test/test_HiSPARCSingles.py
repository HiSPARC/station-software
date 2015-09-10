import sys
sys.path.append("..")
import unittest

from HiSPARCSingles import HiSPARCSingles

from load_message import load_hisparc_message


class TestHiSPARCSingles(unittest.TestCase):

    def test_singles(self):
        singles = load_hisparc_message('test_data/Singles.txt')
        hisparcsingles = HiSPARCSingles([5, singles])
        hisparcsingles.uploadCode = 'SIN'
        singlesdata = hisparcsingles.parseMessage()


if __name__ == '__main__':
    unittest.main()
